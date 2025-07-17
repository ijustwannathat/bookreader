from django.urls import path

from .views import BookDetailView, BookView

urlpatterns = [
    path("", BookView.as_view(), name="book-view"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail-view"),
]
