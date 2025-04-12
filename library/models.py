from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from taggit.managers import TaggableManager

from library.model_utils import unique_slugify


class Book(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='books')
    genres = models.ManyToManyField('Genre', blank=True, related_name='books')

    author = models.ManyToManyField('Author', blank=True, related_name='books')

    book_title = models.CharField(max_length=100)
    slug = models.CharField( max_length=255, unique=True)
    annotation = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True, related_name='books')
    sequence = models.ManyToManyField('Sequence', blank=True, related_name='books')
    book_file = models.FileField(upload_to='books/')
    coverpage = models.ImageField(upload_to='coverpages/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title

    # def get_absolute_url(self):
    #     return reverse('articles_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.book_title)
        super().save(*args, **kwargs)


class Sequence(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(null=True, blank=True)
    lat_name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.lat_name = slugify(self.name)
        super().save(*args, **kwargs)


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=50, blank=True, null=True)
    home_pages = models.CharField(max_length=500, blank=True, null=True)
    emails = models.CharField(max_length=500, blank=True, null=True)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.pk} {self.first_name} {self.last_name} {self.middle_name}'

    def get_absolute_url(self):
        return reverse('library:author', kwargs={'author_slug': self.slug})

    def save(self, *args, **kwargs):
        if self.first_name and self.middle_name and self.last_name:
            p_slug = f'{self.first_name} {self.middle_name} {self.last_name}'
        elif self.first_name and self.last_name:
            p_slug = f'{self.first_name} {self.last_name}'
        elif self.nickname:
            p_slug = self.nickname
        else:
            p_slug = 'Noname author'
        if not self.slug:
            self.slug = unique_slugify(self, p_slug)
        super().save(*args, **kwargs)


class Genre(models.Model):
    genre_short = models.CharField(max_length=50)
    genre_rus = models.CharField(max_length=50)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.genre_rus

    # def get_absolute_url(self):
    #     return reverse('articles_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.genre_rus)
        super().save(*args, **kwargs)
