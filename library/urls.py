from django.urls import path

from library import views

app_name = 'library'

urlpatterns = [
    path('change-read-status/<int:book_pk>/', views.change_read_status, name='change_read_status'),
    path('upload-book/', views.UploadBook.as_view(), name='upload_book'),
    path('download-book/<slug:book_slug>/', views.DownloadBook.as_view(), name='download_book'),
    path('authors/', views.AuthorsView.as_view(), name='authors'),
    path('author/<slug:author_slug>/', views.AuthorView.as_view(), name='author'),
    path('book/<slug:book_slug>/', views.BookView.as_view(), name='book'),
    path('delete-book/<int:pk>/', views.DeleteBook.as_view(), name='delete_book'),
    path('genres/', views.GenresView.as_view(), name='genres'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),
    path('', views.HomeView.as_view(), name='home'),
]
