import logging

from django import forms
from django.core.exceptions import ValidationError

from library.models import Book

log = logging.getLogger(__name__)

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_file']

    def clean(self):
        book_file_name = self.cleaned_data['book_file'].name
        if book_file_name.split('.')[-1] != 'fb2':
            raise ValidationError('Книга должна быть с разрешением fb2')
        return super().clean()


