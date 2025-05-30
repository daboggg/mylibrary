from django import template
from django.db.models.aggregates import Count

from library.models import Genre, Book, Author
from users.models import User

register = template.Library()

@register.inclusion_tag("library/inclusion_tags/book_card_avers.html")
def get_book_card_avers(book: Book):
    return {
        'authors': book.author.all(),
        'sequence': book.sequence.all(),
        'tags': book.tags.all(),
        'genres': book.genres.all(),
    }

@register.inclusion_tag("library/inclusion_tags/book_card_revers.html")
def get_book_card_reverse(book: Book):
    return {
        'annotation': book.annotation,
        'book_title': book.book_title,
        'authors': book.author.all(),
    }

@register.inclusion_tag("library/inclusion_tags/pagination.html", takes_context=True)
def pagination(context):
    return {
        'page_obj': context['page_obj'],
        'paginator': context['paginator'],
        'request': context['request'],

    }

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def get_genres(arg=None):
    if arg == 'most_popular':
        return Genre.objects.filter(books__isnull=False).annotate(book_count=Count('books')).order_by('-book_count')[:7]
    else:
        return Genre.objects.filter(books__isnull=False).annotate(book_count=Count('books')).order_by('-book_count')

@register.simple_tag
def get_authors(arg=None):
    if arg == 'most_popular':
        return Author.objects.filter(books__isnull=False).annotate(book_count=Count('books')).order_by('-book_count')[:7]
    else:
        return Author.objects.filter(books__isnull=False).annotate(book_count=Count('books')).order_by('-book_count')

@register.simple_tag
def get_total_books():
    return Book.objects.count()

@register.filter
def get_author_name(author: Author):
    nickname = f'({author.nickname})' if author.nickname else ''
    if author.first_name and author.last_name:
        if author.middle_name:
            return f'{author.last_name} {author.first_name} {author.middle_name} {nickname}'
        else:
            return f'{author.last_name} {author.first_name} {nickname}'
    elif author.nickname:
        return author.nickname
    else:
        return 'No author'

@register.simple_tag
def get_alphabet_for_search_author():
    return "АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"

@register.simple_tag
def is_read(book: Book, user: User):

    return user.id in book.ids.values_list('user_id', flat=True)

