# Generated by Django 5.1.1 on 2024-11-16 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_blob_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='blob_path',
        ),
    ]
