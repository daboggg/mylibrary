from pprint import pprint

import chardet
import xmltodict
from bs4 import BeautifulSoup as bs, Tag, BeautifulSoup
from django.db.models.fields.files import FieldFile




def get_soup_from_fb2(file:FieldFile)-> BeautifulSoup:

    encoding = chardet.detect(file.read()).get('encoding')

    file.seek(0)
    soup = bs(file.read().decode(encoding=encoding), 'xml')
    # pprint(soup)
    # title_info = soup.find('title-info')
    # print(type(title_info))
    # pprint(title_info.find_all('author'))
    # print(type(title_info.find_all('author')))

    # result_dict = xmltodict.parse(str(title_info))

    # if soup.select('title-info annotation'):
    #     result_dict['title-info']['annotation'] = " ".join(soup.select('title-info annotation')[0].text.split())
    #
    # return result_dict.get('title-info')
    return soup