from django import forms

from library.models import Book


class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_file']