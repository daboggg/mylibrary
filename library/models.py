from django.db import models

class Book(models.Model):
    genres = models.ManyToManyField('Genre', blank=True, related_name='books')

    author = models.ManyToManyField('Author', blank=True, related_name='books')

    book_title = models.CharField(max_length=100)
    annotation = models.TextField()
    keywords = models.CharField(max_length=300)
    sequence = models.CharField(max_length=100)
    book_file = models.FileField(upload_to='books/')


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    home_page = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'


class Genre(models.Model):
    genre_short = models.CharField(max_length=50)
    genre_rus = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_rus

