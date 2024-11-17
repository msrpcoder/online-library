import logging
import os
from datetime import datetime

from django.db import transaction
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView

from books.models import Genre, Author, Publisher, Language, Book
from utils import save_pdf_thumbnail, get_pdf_pages_count
from utils.views import BaseLoginView

logger = logging.getLogger()


class AuthorAddView(BaseLoginView, TemplateView):
    template_name = 'add-author.html'

    def get_context_data(self, **kwargs):
        author = None
        author_id = kwargs.get('id', None)
        if author_id:
            try:
                author = Author.objects.get(pk=author_id)
            except Author.DoesNotExist:
                logger.warning(f"Book {author_id} doesn't exists.")

        return {
            **kwargs,
            'page_header': 'Add Author',
            'author': author
        }

    def post(self, request, **kwargs):
        author_id = kwargs.get('id', None)
        name = request.POST.get('name', '')

        if not name:
            return self.get(request, errors={'name': 'This field is required.'})
        else:
            author = None
            if author_id:
                try:
                    author = Author.objects.get(pk=author_id)
                except Author.DoesNotExist:
                    logger.warning("Author don't exist.")

            if not author:
                author = Author()

            author.name = name
            author.save()

            return HttpResponseRedirect(reverse('author-list'))


class PublisherAddView(BaseLoginView, TemplateView):
    template_name = 'add-publisher.html'

    def get_context_data(self, **kwargs):
        publisher = None
        publisher_id = kwargs.get('id', None)
        if publisher_id:
            try:
                publisher = Publisher.objects.get(pk=publisher_id)
            except Publisher.DoesNotExist:
                logger.warning(f"Publisher {publisher_id} doesn't exists.")

        return {
            **kwargs,
            'page_header': 'Add Publisher',
            'publisher': publisher
        }

    def post(self, request, **kwargs):
        publisher_id = kwargs.get('id', None)
        name = request.POST.get('name', '')

        if not name:
            return self.get(request, errors={'name': 'This field is required.'})
        else:
            publisher = None
            if publisher_id:
                try:
                    publisher = Publisher.objects.get(pk=publisher_id)
                except Publisher.DoesNotExist:
                    logger.warning("Publisher don't exist.")

            if not publisher:
                publisher = Publisher()

            publisher.name = name
            publisher.save()

            return HttpResponseRedirect(reverse('publisher-list'))


class LanguageAddView(BaseLoginView, TemplateView):
    template_name = 'add-language.html'

    def get_context_data(self, **kwargs):
        language = None
        language_id = kwargs.get('id', None)
        if language_id:
            try:
                language = Language.objects.get(pk=language_id)
            except Language.DoesNotExist:
                logger.warning(f"Language {language_id} doesn't exists.")

        return {
            **kwargs,
            'page_header': 'Add Language',
            'language': language
        }

    def post(self, request, **kwargs):
        language_id = kwargs.get('id', None)
        name = request.POST.get('name', '')

        if not name:
            return self.get(request, errors={'name': 'This field is required.'})
        else:
            language = None
            if language_id:
                try:
                    language = Language.objects.get(pk=language_id)
                except Language.DoesNotExist:
                    logger.warning("Language don't exist.")

            if not language:
                language = Language()

            language.name = name
            language.save()

            return HttpResponseRedirect(reverse('language-list'))


# Create your views here.
class BookAddView(BaseLoginView, TemplateView):
    template_name = "book-form.html"

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'genre': self.request.GET.get('genre', ''),
            'page_header': 'Add book',
            'genres': Genre.objects.all(),
            'publishers': Publisher.objects.all(),
            'authors': Author.objects.all(),
            'languages': Language.objects.all()
        }

    def post(self, request, **kwargs):
        data = request.POST

        errors = {}
        isbn_no = data.get('isbn-number', '')
        if not isbn_no:
            errors['isbn-number'] = 'This field is required.'

        title = data.get('title', '')
        if not title:
            errors['title'] = 'This field is required.'

        author_id = data.get('author', '')
        if not author_id:
            errors['author'] = 'This field is required'

        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            errors['author'] = 'Author does not exists'

        language_id = data.get('language', '')
        if not language_id:
            errors['language'] = 'This field is required'

        try:
            language = Language.objects.get(pk=language_id)
        except Language.DoesNotExist:
            errors['language'] = 'Language does not exist'

        genre_id = data.get('genre', '')
        if not genre_id:
            errors['genre'] = 'This field is required'

        try:
            genre = Genre.objects.get(pk=genre_id)
        except Genre.DoesNotExist:
            errors['genre'] = 'Genre does not exist'

        publisher_id = data.get('publisher', '')
        if not publisher_id:
            errors['publisher'] = 'This field is required'

        try:
            publisher = Publisher.objects.get(pk=publisher_id)
        except Publisher.DoesNotExist:
            errors['publisher'] = 'Publisher does not exist'

        publication_date_raw = data.get('publicationDate', '')
        if not publication_date_raw:
            errors['publication_date'] = 'This field is required'

        publication_date = datetime.strptime(publication_date_raw, '%Y-%m-%d').date()

        pdf_file = request.FILES['pdf']
        if not pdf_file:
            errors['pdf'] = 'This field is required'

        if len(errors) > 0:
            return self.get(request, errors=errors)
        else:
            # upload_file
            with transaction.atomic():
                book = Book()
                book.language = language
                book.genre = genre
                book.publisher = publisher
                book.publication_date = publication_date
                book.title = title
                book.author = author
                book.isbn_no = isbn_no

                book.save()

                book_media_path = os.path.join(settings.MEDIA_ROOT, str(book.isbn_no))
                os.makedirs(book_media_path)

                pdf_path = os.path.join(book_media_path, 'book.pdf')
                with open(pdf_path, 'wb') as fp:
                    for chunk in pdf_file.chunks():
                        fp.write(chunk)

                thumbnail_path = os.path.join(book_media_path, 'thumbnail.png')
                save_pdf_thumbnail(pdf_path, thumbnail_path)

                book.page_count = get_pdf_pages_count(pdf_path)
                book.save()

            return HttpResponseRedirect(reverse('book-catalog'))


class AuthorListView(BaseLoginView, TemplateView):
    template_name = 'list-authors.html'

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'Authors',
            'authors': Author.objects.all()
        }


class PublisherListView(BaseLoginView, TemplateView):
    template_name = 'list-publishers.html'

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'Publishers',
            'publishers': Publisher.objects.all()
        }


class LanguageListView(BaseLoginView, TemplateView):
    template_name = 'list-languages.html'

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'Languages',
            'languages': Language.objects.all()
        }


class GenreDeleteView(BaseLoginView):
    def post(self, request, **kwargs):
        genre_id = kwargs.get('id', request.POST.get('id', ''))

        try:
            genre = Genre.objects.get(pk=genre_id)
        except Genre.DoesNotExist:
            logger.warning(f"Object with id: {genre_id} doesn't exist.")
        else:
            genre.delete()

        return HttpResponseRedirect(redirect_to=reverse('genre-list'))


class AuthorDeleteView(BaseLoginView):
    def post(self, request, **kwargs):
        author_id = kwargs.get('id', request.POST.get('id', ''))

        try:
            author = Author.objects.get(pk=author_id)
        except Genre.DoesNotExist:
            logger.warning(f"Object with id: {author_id} doesn't exist.")
        else:
            author.delete()

        return HttpResponseRedirect(redirect_to=reverse('author-list'))


class PublisherDeleteView(BaseLoginView):
    def post(self, request, **kwargs):
        publisher_id = kwargs.get('id', request.POST.get('id', ''))

        try:
            publisher = Publisher.objects.get(pk=publisher_id)
        except Publisher.DoesNotExist:
            logger.warning(f"Object with id: {publisher_id} doesn't exist.")
        else:
            publisher.delete()

        return HttpResponseRedirect(redirect_to=reverse('publisher-list'))


class LanguageDeleteView(BaseLoginView):
    def post(self, request, **kwargs):
        language_id = kwargs.get('id', request.POST.get('id', ''))

        try:
            language = Language.objects.get(pk=language_id)
        except Language.DoesNotExist:
            logger.warning(f"Object with id: {language_id} doesn't exist.")
        else:
            language.delete()

        return HttpResponseRedirect(redirect_to=reverse('language-list'))


class GenreAddView(BaseLoginView, TemplateView):
    template_name = 'add-genre.html'

    def get_context_data(self, **kwargs):
        genre = None
        genre_id = kwargs.get('id', None)
        if genre_id:
            try:
                genre = Genre.objects.get(pk=genre_id)
            except Genre.DoesNotExist:
                logger.warning(f"Genre {genre_id} doesn't exists.")

        return {
            **kwargs,
            'page_header': 'Add Genre',
            'genre': genre
        }

    def post(self, request, **kwargs):
        genre_id = kwargs.get('id', None)
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if not name:
            return self.get(request, errors={'name': 'This field is required.'})
        else:
            genre = None
            if genre_id:
                try:
                    genre = Genre.objects.get(pk=genre_id)
                except Genre.DoesNotExist:
                    logger.warning("Genre don't exist.")

            if not genre:
                genre = Genre()

            genre.name = name
            genre.description = description

            genre.save()

            return HttpResponseRedirect(reverse('genre-list'))


class GenreListView(BaseLoginView, TemplateView):
    template_name = 'list-genres.html'

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'Genres',
            'genres': Genre.objects.all()
        }


class BookCatalogView(BaseLoginView, TemplateView):
    template_name = "book-catalog.html"

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'page_header': 'Book Catalog',
            'genres': Genre.objects.all()
        }


class BookDetailsView(BaseLoginView, TemplateView):
    template_name = "book-details.html"

    def get_context_data(self, **kwargs):
        book_id = kwargs.get('book_id', None)
        assert book_id, 'id parameter is required'

        return {
            **kwargs,
            'book': Book.objects.get(pk=book_id)
        }


class BookDeleteView(BaseLoginView, TemplateView):
    def post(self, request, **kwargs):
        book_id = kwargs.get('book_id')

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            logger.warning(f"Book with id {book_id} does not exist")
        else:
            with transaction.atomic():
                book.delete_book_artifacts()
                book.delete()

        return HttpResponseRedirect(reverse('book-catalog'))


class BookPreviewView(BaseLoginView, TemplateView):
    template_name = "book-preview.html"

    def get_context_data(self, **kwargs):
        book = None
        book_id = kwargs.get('book_id', None)
        if book_id:
            try:
                book = Book.objects.get(pk=book_id)
            except Book.DoesNotExist:
                logger.warning(f"Book {book_id} doesn't exists.")

        return {
            **kwargs,
            'page_header': 'Preview book',
            'book': book
        }