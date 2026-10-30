import os
from django.db.models import F, Count, Sum
from django.http import FileResponse, Http404
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import EpubBook, Genre
from .serializers import (
    EpubBookListSerializer,
    EpubBookDetailSerializer,
    GenreSerializer,
)
from .scanner import scan_epub_directory


class EpubBookFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(method="filter_multi_genres")
    genres = django_filters.CharFilter(method="filter_multi_genres")
    exclude_genres = django_filters.CharFilter(method="filter_exclude_genres")
    author = django_filters.CharFilter(field_name="author", lookup_expr="icontains")
    status = django_filters.CharFilter(method="filter_multi_status")
    language = django_filters.CharFilter(method="filter_multi_language")

    def filter_multi_genres(self, queryset, name, value):
        if not value:
            return queryset
        slugs = [s.strip().lower() for s in value.split(",") if s.strip()]
        if not slugs:
            return queryset
        for slug in slugs:
            queryset = queryset.filter(genres__slug=slug)
        return queryset.distinct()

    def filter_exclude_genres(self, queryset, name, value):
        if not value:
            return queryset
        slugs = [s.strip().lower() for s in value.split(",") if s.strip()]
        if not slugs:
            return queryset
        return queryset.exclude(genres__slug__in=slugs).distinct()

    def filter_multi_status(self, queryset, name, value):
        if not value:
            return queryset
        statuses = [s.strip().lower() for s in value.split(",") if s.strip()]
        if not statuses:
            return queryset
        return queryset.filter(status__in=statuses)

    def filter_multi_language(self, queryset, name, value):
        if not value:
            return queryset
        langs = [s.strip().lower() for s in value.split(",") if s.strip()]
        if not langs:
            return queryset
        return queryset.filter(language__in=langs)

    class Meta:
        model = EpubBook
        fields = ["genre", "genres", "exclude_genres", "author", "status", "language"]


class EpubBookListView(generics.ListAPIView):
    """List EPUB books with search, genre filter, and ordering."""
    queryset = EpubBook.objects.prefetch_related("genres").all()
    serializer_class = EpubBookListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EpubBookFilter
    search_fields = ["title", "author", "description"]
    ordering_fields = ["created_at", "download_count", "title", "file_size_bytes", "total_chapters"]
    ordering = ["-created_at"]


class EpubBookDetailView(generics.RetrieveAPIView):
    """Retrieve single EPUB book detail."""
    queryset = EpubBook.objects.prefetch_related("genres").all()
    serializer_class = EpubBookDetailSerializer


class EpubDownloadView(APIView):
    """Direct secure download endpoint without exposing local disk path."""

    def get(self, request, pk):
        try:
            book = EpubBook.objects.get(pk=pk)
        except EpubBook.DoesNotExist:
            raise Http404("Buku ePub tidak ditemukan.")

        if not os.path.exists(book.file_path):
            raise Http404("File ePub pada storage server tidak ditemukan.")

        # Increment atomic download counter
        EpubBook.objects.filter(pk=pk).update(download_count=F("download_count") + 1)

        filename = os.path.basename(book.file_path)
        # Handle UTF-8 / ASCII safe filename header
        response = FileResponse(open(book.file_path, "rb"), content_type="application/epub+zip")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response


class TriggerScanView(APIView):
    """Trigger scanning of local ePub directory."""

    def post(self, request):
        default_folder = r"C:\Users\Dafit Fernandus\Downloads"
        folder_path = request.data.get("folder_path") or default_folder
        force_update = bool(request.data.get("force_update", False))

        result = scan_epub_directory(folder_path, force_update=force_update)
        if result["status"] == "error":
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)


class GenreListView(generics.ListAPIView):
    """List all genres with count of books."""
    queryset = Genre.objects.annotate(books_count=Count("books")).filter(books_count__gt=0).order_by("-books_count")
    serializer_class = GenreSerializer
    pagination_class = None


class StatsView(APIView):
    """Overall statistics for dashboard / header badge."""

    def get(self, request):
        total_books = EpubBook.objects.count()
        total_downloads = EpubBook.objects.aggregate(total=Sum("download_count"))["total"] or 0
        total_bytes = EpubBook.objects.aggregate(total=Sum("file_size_bytes"))["total"] or 0
        total_genres = Genre.objects.filter(books__isnull=False).distinct().count()

        return Response({
            "total_books": total_books,
            "total_downloads": total_downloads,
            "total_size_mb": round(total_bytes / (1024 * 1024), 2),
            "total_genres": total_genres,
        })
