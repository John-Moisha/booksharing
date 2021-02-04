"""booksharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),

    path('books/create/', views.book_create, name='book-create'),
    path('books/list/', views.books_list, name='books-list'),
    path('books/update/<int:pk>/', views.book_update, name='book-update'),
    path('books/delete/<int:pk>/', views.book_delete, name='book-delete'),

    path('books/authors/create/', views.author_create, name='author-create'),
    path('books/authors/list/', views.authors_list, name='authors-list'),
    path('books/authors/update/<int:pk>/', views.author_update, name='author-update'),
    path('books/authors/delete/<int:pk>/', views.author_delete, name='author-delete'),
]
