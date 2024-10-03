from django.shortcuts import render
from django.views.generic import TemplateView

from utils.views import BaseLoginView


# Create your views here.
class BookAddView(BaseLoginView, TemplateView):
    template_name = "book-form.html"


class BookCatalogView(BaseLoginView, TemplateView):
    template_name = "book-catalog.html"


class BookDetailsView(BaseLoginView, TemplateView):
    template_name = "book-details.html"


class BookPreviewView(BaseLoginView, TemplateView):
    template_name = "book-preview.html"
