from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from library.forms import BookUploadForm
from library.models import Book


def home(request):
    return render(request, 'library/home.html')


class UploadBook(CreateView):
    form_class = BookUploadForm
    template_name = 'library/upload_book.html'
    success_url = reverse_lazy('library:home')

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
        form.instance.genre = 'LKJLKJ'
        return super().form_valid(form)
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Добавление статьи',
    # }
