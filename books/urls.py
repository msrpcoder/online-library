from django.urls import path

from books.views import BookAddView, BookCatalogView, BookPreviewView, BookDetailsView, GenreAddView, GenreListView, \
    GenreDeleteView, AuthorAddView, AuthorListView, AuthorDeleteView, PublisherListView, PublisherAddView, \
    PublisherDeleteView, LanguageListView, LanguageAddView, LanguageDeleteView, BookDeleteView, BookSearchView, \
    GenreSearchView, AuthorSearchView, PublisherSearchView, LanguageSearchView

urlpatterns = [
    # genre urlconfig
    path('genres/<int:id>/delete', GenreDeleteView.as_view(), name='genre-delete'),
    path('genres/<int:id>/edit', GenreAddView.as_view(), name='genre-edit'),
    path('genres/search', GenreSearchView.as_view(), name='genre-search'),
    path('genres/add', GenreAddView.as_view(), name='genre-add'),
    path('genres', GenreListView.as_view(), name='genre-list'),
    # author urlconfig
    path('authors', AuthorListView.as_view(), name='author-list'),
    path('authors/search', AuthorSearchView.as_view(), name='author-search'),
    path('authors/add', AuthorAddView.as_view(), name='author-add'),
    path('authors/<int:id>/edit', AuthorAddView.as_view(), name='author-edit'),
    path('authors/<int:id>/delete', AuthorDeleteView.as_view(), name='author-delete'),
    # publisher urlconfig
    path('publishers', PublisherListView.as_view(), name='publisher-list'),
    path('publishers/search', PublisherSearchView.as_view(), name='publisher-search'),
    path('publishers/add', PublisherAddView.as_view(), name='publisher-add'),
    path('publishers/<int:id>/edit', PublisherAddView.as_view(), name='publisher-edit'),
    path('publishers/<int:id>/delete', PublisherDeleteView.as_view(), name='publisher-delete'),
    # language urlconfig
    path('languages', LanguageListView.as_view(), name='language-list'),
    path('languages/search', LanguageSearchView.as_view(), name='language-search'),
    path('languages/add', LanguageAddView.as_view(), name='language-add'),
    path('languages/<int:id>/edit', LanguageAddView.as_view(), name='language-edit'),
    path('languages/<int:id>/delete', LanguageDeleteView.as_view(), name='language-delete'),
    # book urlconfig
    path('add', BookAddView.as_view(), name='book-add'),
    path('search', BookSearchView.as_view(), name='book-search'),
    path('catalog', BookCatalogView.as_view(), name='book-catalog'),
    path('<int:book_id>/details', BookDetailsView.as_view(), name='book-details'),
    path('<int:book_id>/preview', BookPreviewView.as_view(), name='book-preview'),
    path('<int:book_id>/edit', BookAddView.as_view(), name='book-edit'),
    path('<int:book_id>/delete', BookDeleteView.as_view(), name='book-delete'),
]