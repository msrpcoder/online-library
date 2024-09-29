from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class BookAddView(TemplateView):
    template_name = "book-form.html"


class BookCatalogView(TemplateView):
    template_name = "book-catalog.html"


class BookDetailsView(TemplateView):
    template_name = "book-details.html"


class BookPreviewView(TemplateView):
    template_name = "book-preview.html"
