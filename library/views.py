from pprint import pprint

from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from library.forms import BookUploadForm
from library.models import Book, Genre, Author
from library.parserFB2 import get_data_from_fb2


def home(request):
    return render(request, 'library/home.html')


a = {'annotation': 'Героев Гуляковского объединяет стремление постичь уникальные '
                   'тайны космических цивилизаций, получить доступ к новым '
                   'знаниям, так необходимым человечеству.',
     'author': {'first-name': 'Евгений',
                'last-name': 'Гуляковский',
                'middle-name': 'Яковлевич'},
     'book-title': 'Стратегия захвата',
     'coverpage': {'image': {'@l:href': '#cover.jpg'}},
     'date': None,
     'genre': 'sf_action',
     'lang': 'ru',
     'src-lang': 'ru'}


class UploadBook(CreateView):
    form_class = BookUploadForm
    template_name = 'library/upload_book.html'
    success_url = reverse_lazy('library:home')

    def prepare_author_data(self, authors)->list|list[dict]:
        if not authors:
            return [{'nickname': 'Неизвестный автор'}]
        elif authors and isinstance(authors, dict):
            authors = [authors]

        for author in authors:

            home_pages = author.get('home-page')
            if home_pages and isinstance(home_pages, list):
                home_pages = ', '.join([hp.strip() for hp in home_pages])
            elif home_pages:
                home_pages = home_pages.strip()
            author['home-page'] = home_pages

            email = author.get('email')
            if email and isinstance(email, list):
                email = ', '.join([e.strip() for e in email])
            elif email:
                email = email.strip()
            author['email'] = email

        return authors

    def create_or_get_authors(self, authors):
        prepared_authors_data = self.prepare_author_data(authors)
        print('после препаред')
        result = []
        print(prepared_authors_data)
        for author in prepared_authors_data:
            try:
                if all([author.get('first-name'), author.get('last-name'), author.get('middle-name')]):
                    print('in try')
                    if author_from_db := Author.objects.get(first_name=author.get('first-name'), last_name=author.get('last-name'),
                                                                middle_name=author.get('middle-name')):
                        if home_page := author.get('home-page'):
                            author_from_db.home_page += f', {home_page}' if author_from_db.home_page else home_page
                            author_from_db = author_from_db.save()
                        result.append(author_from_db)



                # elif author.get('first_name') and author.get('last_name'):
                #     if authors_from_db := Author.objects.filter(first_name=author.get('first_name'), last_name=author.get('last_name')):
                #         result.append(authors_from_db.first())
                # elif author.get('nickname'):
                #     if authors_from_db := Author.objects.filter(nickname=author.get('nickname')):
                #         result.append(authors_from_db.first())
            except:
                print('in except')
                # todo ИСПРАВИТЬ!!!!!!!!!!!!!!!!!!!!!
                a = Author()
                a.first_name = author.get('first-name')
                a.last_name = author.get('last-name')
                a.middle_name = author.get('middle-name')
                a.save()
                print('ERROR')
                result.append(a)
            return result

    def form_valid(self, form):



        print('in form_valid')
        book_data = get_data_from_fb2(form.instance.book_file)

        book_title = book_data.get('book-title').lower() if book_data.get('book-title') else None

        print(book_title)

        if Book.objects.filter(book_title__iexact=book_title):
            print('in if')
            form.add_error('book_file', ValidationError('Такая книга уже существует'))
            return super().form_invalid(form)


        # pprint(book_data)
        # form.instance.genre = book_data.get('genre')
        # form.instance.genres = book_data.get('genre')
        genres = book_data.get('genre')
        genres = genres if isinstance(genres, list) else [genres]
        genres = Genre.objects.filter(genre_short__in=genres)

        authors = book_data.get('author')

        authors = self.create_or_get_authors(authors)
        # pprint(authors)


        book: Book = form.save()
        book.genres.set(genres)
        book.author.set(authors)

        form.instance.annotation = book_data.get('annotation')
        form.instance.book_title = book_data.get('book-title')
        return super().form_valid(form)
