from django.urls import path

from books.views import BookAddView, BookCatalogView, BookPreviewView, BookDetailsView

urlpatterns = [
    path('add', BookAddView.as_view(), name='book-add'),
    path('catalog', BookCatalogView.as_view(), name='book-catalog'),
    path('<int:book_id>/details', BookDetailsView.as_view(), name='book-details'),
    path('<int:book_id>/preview', BookPreviewView.as_view(), name='book-preview'),
]