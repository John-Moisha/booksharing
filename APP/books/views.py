from django.http import HttpResponse

from books.models import Book
from books.models import Author


# Create your views here.
def book_list(request):
    response_content = ''
    # Book.objects.all() - SELECT * FROM books_book;
    for book in Book.objects.all():
        response_content += f'ID: {book.id},' \
                            f' Author: {book.author} <br/>'
    return HttpResponse(response_content)


# first_name, last_name, date_of_birth, date_of_death,
# country, gender, native_language

def author_list(request):
    response_content = ''
    for author in Author.objects.all():
        response_content += f'ID: {author.id},' \
                            f' Author: <storng>{author.first_name} ' \
                            f'{author.last_name}</storng>,' \
                            f'B-Day:<i>{author.date_of_birth}</i>,' \
                            f'D-Day:<i>{author.date_of_death or "oops"}</i>,' \
                            f' Gender: {author.gender},' \
                            f' Country: {author.country},' \
                            f' Native language: {author.native_language}'
    return HttpResponse(response_content)
