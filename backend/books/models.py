from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    """Genre or tag categorized from EPUB subject metadata."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or "general"
        super().save(*args, **kwargs)


class EpubBook(models.Model):
    """Metadata and local path tracking for an EPUB file."""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=500, db_index=True)
    original_title = models.CharField(max_length=500, blank=True, default="")
    author = models.CharField(max_length=255, default="Unknown", db_index=True)
    description = models.TextField(blank=True, default="")
    language = models.CharField(max_length=50, default="en", db_index=True)
    genres = models.ManyToManyField(Genre, blank=True, related_name="books")

    status = models.CharField(max_length=50, default="Completed")
    source_url = models.CharField(max_length=500, blank=True, default="")
    identifier = models.CharField(max_length=255, blank=True, default="")

    file_path = models.CharField(max_length=1000, blank=True, db_index=True)
    epub_file = models.FileField(upload_to="epubs/", blank=True, null=True, help_text="Upload .epub directly via admin")
    file_size_bytes = models.BigIntegerField(default=0)
    total_chapters = models.PositiveIntegerField(default=0)
    total_characters = models.PositiveIntegerField(default=0)
    
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    cover_url = models.CharField(max_length=500, blank=True, default="")

    download_count = models.PositiveIntegerField(default=0, db_index=True)
    views_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=4.8)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.author})"

    @property
    def absolute_file_path(self):
        if self.epub_file:
            return self.epub_file.path
        return self.file_path

    @property
    def file_size_mb(self):
        if not self.file_size_bytes:
            return 0.0
        return round(self.file_size_bytes / (1024 * 1024), 2)

    @property
    def display_cover(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_url:
            return self.cover_url
        return "/assets/cover_placeholder.svg"

    @property
    def chars_display(self):
        if not self.total_characters:
            return "120K"
        if self.total_characters >= 1000000:
            return f"{round(self.total_characters / 1000000, 1)}M"
        if self.total_characters >= 1000:
            return f"{round(self.total_characters / 1000, 1)}K"
        return str(self.total_characters)
