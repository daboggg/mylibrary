from django.db import models

class Book(models.Model):
    genre = models.CharField(max_length=100)
    book_title = models.CharField(max_length=100)
    book_file = models.FileField(upload_to='books/')
