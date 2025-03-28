from django.contrib.auth import get_user_model
from django.db import models

class Book(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='books')
    genres = models.ManyToManyField('Genre', blank=True, related_name='books')

    author = models.ManyToManyField('Author', blank=True, related_name='books')

    book_title = models.CharField(max_length=100)
    annotation = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True)
    sequence = models.CharField(max_length=100, blank=True, null=True)
    book_file = models.FileField(upload_to='books/')
    coverpage = models.ImageField(upload_to='coverpages/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=50, blank=True, null=True)
    home_pages = models.CharField(max_length=500, blank=True, null=True)
    emails = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.pk} {self.first_name} {self.last_name} {self.middle_name}'


class Genre(models.Model):
    genre_short = models.CharField(max_length=50)
    genre_rus = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_rus

