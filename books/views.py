import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from books.models import Genre
from utils.views import BaseLoginView

logger = logging.getLogger()


# Create your views here.
class BookAddView(BaseLoginView, TemplateView):
    template_name = "book-form.html"

    def _get_genres(self):
        return ['Religion', 'Sports']

    def get_context_data(self, **kwargs):
        return {
            **kwargs,
            'genre': self.request.GET.get('genre', ''),
            'page_header': 'Add book',
            'genres': self._get_genres()
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
