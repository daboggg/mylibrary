import base64
import logging

import xmltodict
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction, IntegrityError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.book_data_utils import check_book_exists, create_or_get_authors, get_genres, get_annotation, get_sequence, \
    get_keywords, get_binary_img
from library.forms import BookUploadForm
from library.parserFB2 import get_soup_from_fb2

log = logging.getLogger(__name__)


def home(request):
    return render(request, 'library/home.html')


class UploadBook(CreateView):
    form_class = BookUploadForm
    template_name = 'library/upload_book.html'
    success_url = reverse_lazy('library:home')


    def form_valid(self, form):

        soup = get_soup_from_fb2(form.instance.book_file)
        title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')


        # проверка на существование книги
        if check_book_exists(title_info):
            form.add_error('book_file', ValidationError('Такая книга уже существует'))
            return super().form_invalid(form)

        authors = create_or_get_authors(title_info)
        # если нет авторов
        if not authors:
            form.add_error('book_file', ValidationError('Книги без автора не может быть'))
            return super().form_invalid(form)

        # сохранение книги в базе данных
        with transaction.atomic():
            for author in authors:
                try:
                    author.save()
                except IntegrityError as e:
                    form.add_error('book_file', ValidationError('ФИО или никнейм автора не уникален'))
                    return super().form_invalid(form)

            form.save()
            form.instance.author.set(authors)
            form.instance.genres.set(get_genres(title_info))
            form.instance.book_title = title_info.get('book-title')
            form.instance.annotation = get_annotation(soup)
            form.instance.keywords = get_keywords(soup)
            form.instance.sequence = get_sequence(title_info)

            # если изображение есть, добавляем его в форму
            if binary_img:=get_binary_img(soup):
                form.instance.coverpage = ContentFile(
                    content=base64.b64decode(binary_img),
                    name=f'{form.instance.book_title}.jpg'
                )

        return super().form_valid(form)
