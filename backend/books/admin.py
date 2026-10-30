from django.contrib import admin
from .models import EpubBook, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(EpubBook)
class EpubBookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "language", "total_chapters", "file_size_mb", "download_count", "created_at"]
    search_fields = ["title", "author", "description"]
    list_filter = ["language", "genres", "created_at"]
    readonly_fields = ["file_size_bytes", "created_at", "updated_at"]
