import xmltodict
from bs4 import BeautifulSoup
from django.contrib.admin.templatetags.admin_list import result_list

from library.models import Author, Genre


def get_genres(soup: BeautifulSoup):
    title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')
    genres = title_info.get('genre')
    if genres:
        if isinstance(genres, str):
            genres = [genres]
    else:
        genres = []
    genres = Genre.objects.filter(genre_short__in=genres)
    return genres


def check_book_exists(soup: BeautifulSoup):
    result = []
    title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')
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




    # result = []
    # authors: ResultSet = soup.find('title-info').find_all('author')
    # book_title = soup.find('title-info').find('book-title')
    #
    # for author in authors:
    #     first_name = author.find('first-name')
    #     last_name = author.find('last-name')
    #     nickname = author.find('nickname')
    #
    #     # проверка по фамилии, имени и названию книги
    #     if first_name and last_name and book_title:
    #         try:
    #             item = Author.objects.get(first_name__iexact=first_name.text.strip(),
    #                                       last_name__iexact=last_name.text.strip(), )
    #             result.append(item.books.filter(book_title__iexact=book_title.text.strip()))
    #         except Author.DoesNotExist:
    #             pass
    #     # проверка по никнейму и названию книги
    #     if nickname and book_title:
    #         try:
    #             item = Author.objects.get(nickname__exact=nickname.text.strip())
    #             result.append(item.books.filter(book_title__iexact=book_title.text.strip()))
    #         except Author.DoesNotExist:
    #             pass
    # return any(result)


def create_or_get_authors(soup: BeautifulSoup):
    title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')
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
                    print(3)
                    result.append(author_from_db)

            elif first_name and last_name:
                if author_from_db := Author.objects.get(first_name__iexact=first_name,
                                                        last_name__iexact=last_name):
                    add_contacts_to_author(author, author_from_db)
                    print(2)
                    result.append(author_from_db)

            elif nickname:
                if author_from_db := Author.objects.get(nickname__iexact=nickname):
                    add_contacts_to_author(author, author_from_db)
                    print(1)
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


def add_contacts_to_author(author, author_from_db):
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


def get_book_title(soup: BeautifulSoup)->str:
    title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')
    return title_info.get('book-title')


def get_annotation(soup: BeautifulSoup)->str|None:
    annotation = soup.find('title-info').find('annotation')
    if annotation:
        return ' '.join(annotation.text.split())
    else:
        return annotation


def get_sequence(soup: BeautifulSoup)->str|None:
    title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')
    sequence = title_info.get('sequence')
    if not sequence:
        return sequence
    if isinstance(sequence, dict):
        sequence = [sequence]

    result = []
    for s in sequence:
        if s.get('@number'):
            result.append(f'{s.get("@name")}:{s.get("@number")}')
        else:
            result.append(s.get('@name'))

    return ', '.join(result)


def get_keywords(soup: BeautifulSoup)->str|None:
    annotation = soup.find('title-info').find('keywords')
    if annotation:
        return annotation.text
    else:
        return annotation



# <coverpage>
#     <image l:href="#cover.jpg"/></coverpage>
# <binary id="cover.jpg" content-type="image/jpg">

def get_binary_img(soup: BeautifulSoup)->str|None:
    title_info = xmltodict.parse(str(soup.find('title-info'))).get('title-info')
    fiction_book = xmltodict.parse(str(soup.find('FictionBook'))).get('FictionBook')
    coverpage = title_info.get('coverpage')
    if not coverpage and coverpage.get('image') and coverpage.get('image').get('@l:href'):
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
