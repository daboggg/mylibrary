import base64
import logging
from uuid import uuid4

import xmltodict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction, IntegrityError
from django.db.models import Count, Q, F
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from pytils.translit import slugify

from library.book_data_utils import check_book_exists, create_or_get_authors, get_genres, get_annotation, get_sequence, \
    get_keywords, get_binary_img, create_and_get_img
from library.forms import BookUploadForm
from library.models import Book, Genre, Author, Sequence
from library.parserFB2 import get_soup_from_fb2
from library.templatetags.library_tags import get_author_name

log = logging.getLogger(__name__)

class GenresView(ListView):
    model = Genre
    template_name = 'library/genres.html'
    context_object_name = 'genres'
    extra_context = {'title': 'Жанры'}

    def get_queryset(self):
        return super().get_queryset().annotate(count=Count('books')).filter(count__gt=0).order_by('genre_rus')
    # paginate_by = 1



class BookView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('author', 'genres', 'sequence', 'tags')


class AuthorView(DetailView):
    model = Author
    template_name = 'library/author_detail.html'
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = self.object.books.all().prefetch_related('genres', 'sequence', 'tags')
        book_data= {}
        for book in books:
            for g in book.genres.all():
                if not g in book_data:
                    book_data[g] = [book]
                else:
                    book_data[g].append(book)
        context['book_data'] = book_data
        return context


class AuthorsView(ListView):
    model = Author
    template_name = 'library/authors.html'
    context_object_name = 'authors'
    extra_context = {'title': 'Авторы'}
    paginate_by = 1

    def get_queryset(self):
        if letter := self.request.GET.get('letter'):
            self.extra_context['query'] = letter
            return Author.objects.filter(Q(last_name__istartswith=letter) | Q(nickname__istartswith=letter))
        elif q := self.request.GET.get('q'):
            self.extra_context['query'] = q
            vector = SearchVector('last_name','first_name', 'nickname')
            query = SearchQuery(q)
            return Author.objects.annotate(search=vector).filter(search=query)
        self.extra_context['query'] = ''
        return []


class HomeView(ListView):
    content_name = ''
    model = Book
    template_name = 'library/home.html'
    context_object_name = 'books'
    paginate_by = 1

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)
        if not self.content_name:
            context['content_name'] = 'Недавно добавленные'
            context['title'] = 'Главная страница'
        else:
            context['content_name'] = self.content_name
            context['title'] = self.content_name
        return context

    def get_queryset(self):
        if self.request.GET:
            if genre_slug := self.request.GET.get('genre_slug'):
                genre = get_object_or_404(Genre, slug=genre_slug)
                self.content_name = f'{genre.genre_rus}'
                return genre.books.prefetch_related('author').order_by('-created_at')
            elif author_slug := self.request.GET.get('author_slug'):
                author = get_object_or_404(Author, slug=author_slug)
                self.content_name = get_author_name(author)
                return author.books.prefetch_related('author').order_by('-created_at')
            elif sequence_lat_name := self.request.GET.get('sequence_lat_name'):
                self.content_name = Sequence.objects.filter(lat_name=sequence_lat_name).first().name
                return Book.objects.prefetch_related('author').filter(sequence__lat_name=sequence_lat_name).distinct().order_by('sequence__number')
            elif tag_name := self.request.GET.get('tag_name'):
                self.content_name = tag_name
                return Book.objects.prefetch_related('author').filter(tags__name=tag_name).order_by('-created_at')
            elif q := self.request.GET.get('q'):
                self.content_name = f'Поиск по "{q}"'
                vector = SearchVector(
                    'genres__genre_rus',
                    'author__first_name',
                    'author__middle_name',
                    'author__last_name',
                    'author__nickname',
                    'book_title',
                    'annotation',
                    'tags__name',
                    'sequence__name',
                )
                query = SearchQuery(q)
                books = (Book.objects.prefetch_related('author').annotate(rank=SearchRank(vector, query))
                        .filter(rank__gt=0).order_by('-rank'))
                return list({book.id: book for book in books}.values())

        return Book.objects.prefetch_related('author').order_by('-created_at')[:7]


class DownloadBook(LoginRequiredMixin, View):
    def get(self, request, book_slug):
        # file_path = get_object_or_404(Book, slug=book_slug).book_file.path
        book = get_object_or_404(Book, slug=book_slug)
        file_path = book.book_file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True,filename=f'{slugify(book.book_title)}.fb2', content_type="application/x-fictionbook+xml")


class UploadBook(LoginRequiredMixin, CreateView):
    form_class = BookUploadForm
    template_name = 'library/upload_book.html'
    success_url = reverse_lazy('library:home')
    extra_context = {'title': 'Добавить книгу'}

    def form_valid(self, form):
        soup = get_soup_from_fb2(form.instance.book_file)
        book_file_instance = form.instance.book_file
        form.instance.book_file = None
        title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')

        # проверка на существование книги
        if check_book_exists(title_info):
            form.add_error(None, ValidationError('Такая книга уже существует'))
            return super().form_invalid(form)

        authors = create_or_get_authors(title_info)
        # если нет авторов
        if not authors:
            form.add_error(None, ValidationError('Книги без автора не может быть'))
            return super().form_invalid(form)

        try:
            # сохранение книги в базе данных
            with transaction.atomic():
                for author in authors:
                    author.save()

                form.save()
                form.instance.owner = self.request.user
                form.instance.book_file = book_file_instance
                form.instance.author.set(authors)
                form.instance.genres.set(get_genres(title_info))
                form.instance.book_title = title_info.get('book-title')
                form.instance.annotation = get_annotation(soup)
                form.instance.tags.set(get_keywords(soup))
                form.instance.sequence.set(get_sequence(title_info))
                form.instance.book_file.name = uuid4().hex[:16]

                # если изображение есть, добавляем его в форму
                if binary_img:=get_binary_img(soup):
                    form.instance.coverpage = ContentFile(
                        content=base64.b64decode(binary_img),
                        name=f'{form.instance.book_title}.jpg'
                    )
                # если изображение нет, создаем с помощью kandinsky и добавляем в форму
                elif binary_img := create_and_get_img(soup):

                        form.instance.coverpage = ContentFile(
                            content=base64.b64decode(binary_img),
                            name=f'{form.instance.book_title}.jpg'
                        )
                        form.instance.book_file = ContentFile(
                            content=str(soup).encode(),
                            name=form.instance.book_file.name.split('/')[-1]
                        )
        except IntegrityError as e:
            log.exception('проблема с сохранением в бд')
            form.add_error(None, ValidationError('ФИО или никнейм автора не уникален'))
            return super().form_invalid(form)
        except Exception as e:
            log.exception('ошибка добавления книги')
            form.add_error(None, ValidationError('Ошибка добавления книги, попробуйте еще раз'))
            return super().form_invalid(form)

        log.info('form is filled')
        return super().form_valid(form)
