import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from books.models import Genre, Author, Publisher, Language
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
                logger.warning(f"Genre {author_id} doesn't exists.")

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
            'page_header': 'Book Catalog'
        }


class BookDetailsView(BaseLoginView, TemplateView):
    template_name = "book-details.html"


class BookPreviewView(BaseLoginView, TemplateView):
    template_name = "book-preview.html"
