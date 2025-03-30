from django import template
from django.db.models.aggregates import Count

from library.models import Genre, Book, Author

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

@register.filter
def get_author_name(author: Author):
    if author.first_name and author.last_name:
        if author.middle_name:
            return f'{author.first_name} {author.middle_name} {author.last_name}'
        else:
            return f'{author.first_name} {author.last_name}'
    elif author.nickname:
        return author.nickname
    else:
        return 'No author'