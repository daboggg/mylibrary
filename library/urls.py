from django.urls import path

from library import views

app_name = 'library'

urlpatterns = [
    path('upload-book/', views.UploadBook.as_view(), name='upload_book'),
    path('download-book/<slug:book_slug>/', views.DownloadBook.as_view(), name='download_book'),
    path('authors/', views.AuthorsView.as_view(), name='authors'),
    path('author/<slug:author_slug>/', views.AuthorView.as_view(), name='author'),
    path('', views.HomeView.as_view(), name='home'),
]