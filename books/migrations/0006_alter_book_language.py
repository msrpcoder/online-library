# Generated by Django 5.1.1 on 2024-11-16 21:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_remove_book_blob_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='books.language'),
        ),
    ]
