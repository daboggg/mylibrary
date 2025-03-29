from django import template
from django.db.models.aggregates import Count

from library.models import Genre, Book

register = template.Library()

@register.simple_tag
def get_genres(arg=None):
    if arg == 'most_popular':
        return Genre.objects.filter(books__isnull=False).annotate(book_count=Count('books')).order_by('-book_count')[:5]
    else:
        return Genre.objects.filter(books__isnull=False).annotate(book_count=Count('books')).order_by('-book_count')

@register.simple_tag
def get_total_books():
    return Book.objects.count()