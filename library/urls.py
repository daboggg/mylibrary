from django.urls import path

from library import views

app_name = 'library'

urlpatterns = [
    path('upload-book', views.UploadBook.as_view(), name='upload_book'),
    path('', views.HomeView.as_view(), name='home'),
]