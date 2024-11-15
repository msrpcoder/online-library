import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Model, CASCADE


# Create your models here.
class TrackedMixin(object):
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)


class Author(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)


class Publisher(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)


class Genre(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)
    description = models.TextField(max_length=500)


class Book(TrackedMixin, Model):
    isbn_no = models.TextField(null=False, primary_key=True, max_length=13)
    author = models.ForeignKey(Author, on_delete=CASCADE, null=False)
    title = models.TextField(null=False, max_length=100)
    language = models.TextField(null=False, max_length=50)
    genre = models.ForeignKey(Genre, null=False, on_delete=CASCADE)
    publisher = models.ForeignKey(Publisher, null=False, on_delete=CASCADE)
    publication_date = models.DateField(null=False)
    blob_path = models.TextField(null=False)

    def save(self, *args, **kwargs):
        if self.publication_date > datetime.date.today():
            raise ValidationError('Publication date can not be a future date.')

        if len(self.language) < 3:
            raise ValidationError('Language should have atleast 3 characters.')

        if len(self.isbn_no) < 3:
            raise ValidationError('ISBN No should have atleast 3 characters.')

        if len(self.title) < 3:
            raise ValidationError('Title should have atleast 3 characters.')

        return super(Book, self).save(*args, **kwargs)
