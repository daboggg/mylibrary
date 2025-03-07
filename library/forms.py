from django import forms
from django.core.exceptions import ValidationError

from library.models import Book


class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_file']

    # def clean(self):
    #     print('in_clean')
    #     if Book.objects.filter(book_title=self.instance.book_title):
    #         print('DAAAAAAA')
    #         raise forms.ValidationError("This book already exists")
    #     return super().clean()


