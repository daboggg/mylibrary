import logging

import xmltodict
from bs4 import BeautifulSoup

from library.kandinsky import get_image_from_kandinsky
from library.models import Author, Genre

log = logging.getLogger(__name__)


def get_genres(title_info: dict) -> list[str] | None:
    """
    возвращает список жанров или None
    """
    genres = title_info.get('genre')
    if genres:
        if isinstance(genres, str):
            genres = [genres]
    else:
        genres = []
    genres = Genre.objects.filter(genre_short__in=genres)
    return genres


def check_book_exists(title_info: dict) -> bool:
    """
    проверяет есть ли в базе данных книга
    """
    result = []
    book_title = title_info.get('book-title')
    authors = title_info.get('author')

    if authors:
        if isinstance(authors, dict):
            authors = [authors]
    else:
        authors = []

    for author in authors:
        first_name = author.get('first-name')
        last_name = author.get('last-name')
        nickname = author.get('nickname')

        # проверка по фамилии, имени и названию книги
        if first_name and last_name and book_title:
            try:
                item = Author.objects.get(first_name__iexact=first_name,
                                          last_name__iexact=last_name, )
                result.append(item.books.filter(book_title__iexact=book_title))
            except Author.DoesNotExist:
                pass
        # проверка по никнейму и названию книги
        if nickname and book_title:
            try:
                item = Author.objects.get(nickname__exact=nickname)
                result.append(item.books.filter(book_title__iexact=book_title))
            except Author.DoesNotExist:
                pass
    return any(result)


def create_or_get_authors(title_info: dict) -> list[Author]:
    """
    получает автора из базы данных,
    если в базе данных нет, создает автора,
    возвращает список авторов
    """
    authors = title_info.get('author')
    if authors:
        if isinstance(authors, dict):
            authors = [authors]
    else:
        authors = []

    result = []
    for author in authors:

        first_name = author.get('first-name')
        last_name = author.get('last-name')
        middle_name = author.get('middle-name')
        nickname = author.get('nickname')
        try:
            if all([first_name, last_name, middle_name]):
                if author_from_db := Author.objects.get(first_name__iexact=first_name,
                                                        last_name__iexact=last_name,
                                                        middle_name__iexact=middle_name):
                    add_contacts_to_author(author, author_from_db)
                    result.append(author_from_db)

            elif first_name and last_name:
                if author_from_db := Author.objects.get(first_name__iexact=first_name,
                                                        last_name__iexact=last_name):
                    add_contacts_to_author(author, author_from_db)
                    result.append(author_from_db)

            elif nickname:
                if author_from_db := Author.objects.get(nickname__iexact=nickname):
                    add_contacts_to_author(author, author_from_db)
                    result.append(author_from_db)
            else:
                raise Author.DoesNotExist
        except Author.DoesNotExist:
            emails = author.get('email')
            home_pages = author.get('home-page')

            result.append(Author(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                nickname=nickname,
                emails=', '.join(emails) if isinstance(emails, list) else emails,
                home_pages=', '.join(home_pages) if isinstance(home_pages, list) else home_pages,
            ))
    return result


def add_contacts_to_author(author, author_from_db) -> None:
    """
    добавляет домашнюю страницу и email к автору
    """
    home_pages = author.get('home-page')
    if home_pages:
        if isinstance(home_pages, str):
            home_pages = set([home_pages])
        else:
            home_pages = set(home_pages)
    else:
        home_pages = set()

    if author_from_db.home_pages:
        author_from_db.home_pages = ', '.join(set(author_from_db.home_pages.split(', ')).union(home_pages))
    else:
        author_from_db.home_pages = ', '.join(home_pages)

    emails = author.get('email')
    if emails:
        if isinstance(emails, str):
            emails = set([emails])
        else:
            emails = set(emails)
    else:
        emails = set()

    if author_from_db.emails:
        author_from_db.emails = ', '.join(
            set(author_from_db.emails.split(', ')).union(emails))
    else:
        author_from_db.emails = ', '.join(emails)


def get_annotation(soup: BeautifulSoup) -> str | None:
    """
    возвращает аннотацию книги
    """
    annotation = soup.find('title-info').find('annotation')
    if annotation:
        return ' '.join(annotation.text.split())
    else:
        return annotation


def get_sequence(title_info: dict) -> str | None:
    """
    если книга входит в серию или в серии,
     возвращает строку с названиями серий через запятую
    """
    sequence = title_info.get('sequence')
    if not sequence:
        return sequence
    if isinstance(sequence, dict):
        sequence = [sequence]

    result = []
    for s in sequence:
        if s.get('@number'):
            result.append(f'{s.get("@name")}: {s.get("@number")}')
        else:
            result.append(s.get('@name'))

    return ', '.join(result)


def get_keywords(soup: BeautifulSoup) -> list[str] | None:
    """
    возвращает строку с ключевыми словами
    """
    keywords = soup.find('title-info').find('keywords')
    if keywords:
        return keywords.text.split(',')
    else:
        return []


def get_binary_img(soup: BeautifulSoup) -> str | None:
    """
    возвращает данные изображения закодированные в base64,
    если изображение присутствует в книге
    """
    fiction_book = xmltodict.parse(str(soup.find('FictionBook'))).get('FictionBook')
    title_info = fiction_book.get('description').get('title-info')
    coverpage = title_info.get('coverpage')
    if not coverpage or  not coverpage.get('image') or not coverpage.get('image').get('@l:href'):
        return None
    href_img = coverpage.get('image').get('@l:href')[1:]
    binary = fiction_book.get('binary')
    if not binary: return None
    if isinstance(binary, dict):
        binary = [binary]
    for bin in binary:
        if bin.get('@id') == href_img:
            return bin.get('#text')
    return None


def create_and_get_img(soup: BeautifulSoup) -> str | None:
    """
    создает изображение, добаляет в книгу и
    возвращает данные изображения закодированные в base64,
    """
    title_info = soup.find('description').find('title-info')
    coverpage = soup.find('coverpage')
    book_title = title_info.find('book-title')
    if book_title: book_title = book_title.text
    annotation = get_annotation(soup)
    if coverpage:
        coverpage.extract()
    coverpage_tag = soup.new_tag("coverpage")
    image_tag = soup.new_tag("image", attrs={"l:href": "#cover.jpg"})
    coverpage_tag.append(image_tag)
    title_info.append(coverpage_tag)

    if binary := soup.find('binary', {"content-type": "image/jpeg", "id": "cover.jpg"}):
        binary.extract()

    if annotation:
        image =  get_image_from_kandinsky(annotation)
    else:
        image =  get_image_from_kandinsky("Обложка для неизвестной книги" if not book_title else book_title)

    binary_tag = soup.new_tag("binary", attrs={"content-type": "image/jpeg", "id": "cover.jpg"},
                              string=image)
    soup.FictionBook.append(binary_tag)

    return image


