# Generated by Django 5.1.6 on 2025-03-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_author_remove_book_author_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='author',
            name='home_page',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
