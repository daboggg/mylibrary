import chardet
import xmltodict
from bs4 import BeautifulSoup as bs
from django.db.models.fields.files import FieldFile


def get_data_from_fb2(file:FieldFile)-> dict:

    encoding = chardet.detect(file.read()).get('encoding')

    file.seek(0)
    soup = bs(file.read().decode(encoding=encoding), 'xml')
    title_info = soup.find('title-info')

    result_dict = xmltodict.parse(str(title_info))

    if soup.select('title-info annotation'):
        result_dict['title-info']['annotation'] = " ".join(soup.select('title-info annotation')[0].text.split())

    return result_dict.get('title-info')