import lxml.html
import chardet
from bs4 import BeautifulSoup as bs

def any_get():
    filename = 'FB2-karr_allen_legkii_sposob_brosit_kurit.fb2'
    with open('KV.fb2', 'rb') as f:
        encoding = chardet.detect(f.read()).get('encoding')
        f.seek(0)
        # print(f.read().decode(encoding=encoding))
        # tree = lxml.html.fromstring(f.read())
        # print(tree)
        soup = bs(f.read().decode(encoding=encoding),'xml')
        annotation = soup.FictionBook.description.annotation.text
        annotation = ' '.join(annotation.split())
        binary = soup.FictionBook.binary.text
        print(binary)
        print(8%3)
        # UnicodeDecodeError

if __name__ == '__main__':
    any_get()