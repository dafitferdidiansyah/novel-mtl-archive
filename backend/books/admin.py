from django.contrib import admin
from django.core.files.base import ContentFile
from .models import EpubBook, Genre, ReaderApp
from .scanner import parse_epub


@admin.register(ReaderApp)
class ReaderAppAdmin(admin.ModelAdmin):
    list_display = ["name", "version", "file_size_mb", "is_active", "download_count", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "version", "description"]
    fields = [
        "name",
        "version",
        "description",
        "apk_file",
        "external_url",
        "icon",
        "is_active",
        "download_count",
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(EpubBook)
class EpubBookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "language", "total_chapters", "file_size_mb", "download_count", "created_at"]
    search_fields = ["title", "author", "description", "original_title"]
    list_filter = ["language", "genres", "created_at"]
    readonly_fields = ["file_size_bytes", "created_at", "updated_at"]
    fields = [
        "epub_file",
        "title",
        "original_title",
        "author",
        "description",
        "language",
        "status",
        "genres",
        "source_url",
        "identifier",
        "cover_image",
        "total_chapters",
        "total_characters",
        "file_size_bytes",
        "created_at",
        "updated_at",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Jika file epub diupload lewat form admin, auto-parse metadata & cover otomatis!
        if obj.epub_file and (not obj.total_chapters or "epub_file" in form.changed_data):
            try:
                parsed = parse_epub(obj.epub_file.path)
                if not obj.title or obj.title == "New Book":
                    obj.title = parsed.get("title") or obj.title
                if not obj.original_title:
                    obj.original_title = parsed.get("original_title", "")
                if not obj.author or obj.author == "Unknown":
                    obj.author = parsed.get("author") or obj.author
                if not obj.description:
                    obj.description = parsed.get("description", "")
                if not obj.source_url:
                    obj.source_url = parsed.get("source_url", "")
                if not obj.identifier:
                    obj.identifier = parsed.get("identifier", "")
                if not obj.language:
                    obj.language = parsed.get("language", "en")
                
                obj.total_chapters = parsed.get("total_chapters", 1)
                obj.total_characters = parsed.get("total_characters", 0)
                obj.file_size_bytes = parsed.get("file_size", obj.epub_file.size)
                obj.file_path = obj.epub_file.path

                # Auto save cover from EPUB if not provided
                if not obj.cover_image and parsed.get("cover_bytes"):
                    cover_name = f"cover_{obj.id}_{parsed.get('cover_filename', 'cover.jpg')}"
                    obj.cover_image.save(cover_name, ContentFile(parsed["cover_bytes"]), save=False)

                obj.save()

                # Sync genres/tags
                for g_name in parsed.get("genres", []):
                    g, _ = Genre.objects.get_or_create(name=g_name)
                    obj.genres.add(g)
            except Exception as e:
                self.message_user(request, f"Notice: Error auto-parsing EPUB metadata: {e}", level="warning")

