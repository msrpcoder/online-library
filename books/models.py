import datetime
import logging
import os.path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model, CASCADE


logger = logging.getLogger()


# Create your models here.
class TrackedMixin(object):
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)


class Author(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)


class Publisher(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)


class Language(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)


class Genre(TrackedMixin, Model):
    name = models.TextField(null=False, max_length=100)
    description = models.TextField(max_length=500)


class Book(TrackedMixin, Model):
    isbn_no = models.TextField(null=False, primary_key=True, max_length=13)
    author = models.ForeignKey(Author, on_delete=CASCADE, null=False)
    title = models.TextField(null=False, max_length=100)
    language = models.ForeignKey(Language, null=False, max_length=50, on_delete=CASCADE)
    genre = models.ForeignKey(Genre, null=False, on_delete=CASCADE)
    publisher = models.ForeignKey(Publisher, null=False, on_delete=CASCADE)
    publication_date = models.DateField(null=False)
    page_count = models.IntegerField(null=False, default=0)
    # blob_path = models.FileField(null=False)

    def save(self, *args, **kwargs):
        if self.publication_date > datetime.date.today():
            raise ValidationError('Publication date can not be a future date.')

        if len(self.language.name) < 3:
            raise ValidationError('Language should have atleast 3 characters.')

        if len(self.isbn_no) < 3:
            raise ValidationError('ISBN No should have atleast 3 characters.')

        if len(self.title) < 3:
            raise ValidationError('Title should have atleast 3 characters.')

        return super(Book, self).save(*args, **kwargs)

    @property
    def thumbnail_exists(self):
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, self.isbn_no, 'thumbnail.png')

        return os.path.exists(thumbnail_path)

    @property
    def media_directory(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.isbn_no))

    def delete_book_artifacts(self):
        try:
            os.remove(os.path.join(self.media_directory, 'book.pdf'))
        except NotADirectoryError:
            logger.warning("Failed to delete book.pdf")

        try:
            os.remove(os.path.join(self.media_directory, 'thumbnail.png'))
        except NotADirectoryError:
            logger.warning("Failed to delete thumbnail.png file")
