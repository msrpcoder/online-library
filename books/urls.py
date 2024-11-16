from django.urls import path

from books.views import BookAddView, BookCatalogView, BookPreviewView, BookDetailsView, GenreAddView, GenreListView, \
    GenreDeleteView, AuthorAddView, AuthorListView, AuthorDeleteView

urlpatterns = [
    path('add', BookAddView.as_view(), name='book-add'),
    path('genres/<int:id>/delete', GenreDeleteView.as_view(), name='genre-delete'),
    path('genres/<int:id>/edit', GenreAddView.as_view(), name='genre-edit'),
    path('genres/add', GenreAddView.as_view(), name='genre-add'),
    path('genres', GenreListView.as_view(), name='genre-list'),
    path('authors', AuthorListView.as_view(), name='author-list'),
    path('authors/add', AuthorAddView.as_view(), name='author-add'),
    path('authors/<int:id>/edit', AuthorAddView.as_view(), name='author-edit'),
    path('authors/<int:id>/delete', AuthorDeleteView.as_view(), name='author-delete'),
    path('catalog', BookCatalogView.as_view(), name='book-catalog'),
    path('<int:book_id>/details', BookDetailsView.as_view(), name='book-details'),
    path('<int:book_id>/preview', BookPreviewView.as_view(), name='book-preview'),
]