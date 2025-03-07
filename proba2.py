from dataclasses import dataclass
from functools import reduce
from typing import Any

import lxml.html
import chardet
from bs4 import BeautifulSoup as bs, NavigableString, Tag
import xmltodict
from dacite import from_dict

a = {'title-info':
         {'genre': ['sf_action', 'sf_action'],
        'author': {'first-name': 'Андрей', 'middle-name': 'Львович', 'last-name': 'Ливадный',
                               'id': 'f079035b-2a80-102a-9ae1-2dfe723fe7c7'}, 'book-title': 'Контрольный выброс',
        'annotation': {
                        'p': 'Если ты один раз попал в Зону Отчуждения, она не отпустит тебя уже никогда. Вот и бывший\n                сталкер Штопор, давно покинувший окрестности Чернобыля, решает вернуться, чтобы забрать из тайника на\n                Кордоне оставленный когда-то хабар. Многое изменилось в Зоне за время его отсутствия, поэтому Штопор\n                нанимает в проводники двух опытных сталкеров\xa0– Инока и Гурона. Они еще не знают, что подписались на\n                смертельно опасное предприятие, в котором противостоять им будут спецслужбы, военные и легендарная\n                сталкерская группировка «Монолит». А у самого Штопора имеется тяжелая и мрачная тайна, которая опаснее,\n                чем все мутанты и коварные ловушки Зоны...'},
        'date': '2009',
          'coverpage': {'image': {'@l:href': '#cover.jpg'}},
          'lang': 'ru',
                    'sequence': {'@name': 'STALKER'}, '#text': 'abbbrrr'}}


def any_get():
    result_dict = {}
    filename = 'FB2-karr_allen_legkii_sposob_brosit_kurit.fb2'
    with open('KV.fb2', 'rb') as f:
        encoding = chardet.detect(f.read()).get('encoding')
        f.seek(0)
        # print(f.read().decode(encoding=encoding))
        # tree = lxml.html.fromstring(f.read())
        # print(tree)
        soup = bs(f.read().decode(encoding=encoding), 'xml')

        title_info = soup.find('title-info')


        result_dict = xmltodict.parse(str(title_info))

        if soup.select('title-info annotation'):
            result_dict['title-info']['annotation'] = " ".join(soup.select('title-info annotation')[0].text.split())

        gnr = result_dict.get('title-info').get('genre')
        gnr = gnr if isinstance(gnr,list) else [gnr]
        print(gnr)



        # for t in ti[0]:
        #     # if t is NavigableString:
        #     # if t is Tag:
        #     if isinstance(t, NavigableString):
        #         print(t)

        res = {}

        # def prepare(elem):
        #     for e in elem:
        #         if isinstance(e, Tag):
        #             prepare(e)
        #         else:
        #
        #             print(e.parent.name, e.text)
        # prepare(ti[0])

        # print(reduce(lambda x, y: x + ' ' + y.text, soup.select('title-info genre'),''))
        # annotation = soup.FictionBook.description.annotation.text
        # annotation = ' '.join(annotation.split())
        # binary = soup.FictionBook.binary.text
        # print(binary)
        # print(8%3)
        # UnicodeDecodeError


if __name__ == '__main__':
    any_get()
