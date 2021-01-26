from django.shortcuts import render
from django.http import HttpResponse

from books.models import Book
from books.models import Author
# Create your views here.

def book_list(request):

    response_content = ''

    for book in Book.objects.all():  # Book.objects.all() - SELECT * FROM books_book;
        response_content += f'ID: {book.id}, Author: {book.author} <br/>'

    return HttpResponse(response_content)

#first_name, last_name, date_of_birth, date_of_death, country, gender, native_language
def author_list(request):

    response_content = ''

    for author in Author.objects.all():
        response_content += f'ID: {author.id},' \
                            f' Author: <storng>{author.first_name} {author.last_name}</storng>,' \
                            f' B-Day: <i>{author.date_of_birth}</i>, D-Day: <i>{author.date_of_death or "oops"}</i>,' \
                            f' Gender: {author.gender},' \
                            f' Country: {author.country},' \
                            f' Native language: {author.native_language}'

    return HttpResponse(response_content)