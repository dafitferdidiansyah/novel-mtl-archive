from django.core.management.base import BaseCommand
from books.scanner import scan_epub_directory


class Command(BaseCommand):
    help = "Scan local folder for EPUB files and save metadata to database"

    def add_arguments(self, parser):
        parser.add_argument("folder_path", type=str, help="Directory path containing .epub files")
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force rescan and update existing books in database",
        )

    def handle(self, *args, **options):
        folder_path = options["folder_path"]
        force = options["force"]
        self.stdout.write(f"Scanning EPUB files in: {folder_path} ...")

        result = scan_epub_directory(folder_path, force_update=force)
        if result["status"] == "error":
            self.stderr.write(self.style.ERROR(result["message"]))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Scan complete! Total files: {result['total_scanned_files']}, "
                f"Added: {result['added']}, Updated: {result['updated']}, "
                f"Errors: {len(result['errors'])}"
            )
        )
        for err in result["errors"]:
            self.stdout.write(self.style.WARNING(f"  - {err['file']}: {err['error']}"))
