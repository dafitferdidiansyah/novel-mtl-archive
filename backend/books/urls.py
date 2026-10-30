from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.EpubBookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.EpubBookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/download/", views.EpubDownloadView.as_view(), name="book-download"),
    path("genres/", views.GenreListView.as_view(), name="genre-list"),
    path("scan/", views.TriggerScanView.as_view(), name="trigger-scan"),
    path("stats/", views.StatsView.as_view(), name="stats"),
    path("apps/", views.ReaderAppListView.as_view(), name="app-list"),
    path("apps/<int:pk>/download/", views.ReaderAppDownloadView.as_view(), name="app-download"),
]
