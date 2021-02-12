from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book, Author, Log
from books.forms import BookForm, AuthorForm


# Create your views here.
def index(requests):
    context = {
        'title': 'Сайт Обмена Книгами',
    }
    return render(requests, 'index.html', context=context)


def books_list(request):
    context = {
        'title': 'Список Книг',
        'books_list': Book.objects.all(),
    }

    return render(request, 'books_list.html', context=context)


def book_create(request):
    form_data = request.POST
    if request.method == 'POST':
        form = BookForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('books-list')
    elif request.method == 'GET':
        form = BookForm()

    context = {
        'title': 'Создать Книгу',
        'form': form,
    }
    return render(request, 'books_create.html', context=context)


def book_update(request, pk):
    instance = get_object_or_404(Book, pk=pk)

    form_data = request.POST
    if request.method == 'POST':
        form = BookForm(form_data, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('books-list')
    elif request.method == 'GET':
        form = BookForm(instance=instance)

    context = {
        'title': 'Редактировать Книгу',
        'message': 'BOOK UPDATE',
        'form': form,
    }

    return render(request, 'books_create.html', context=context)


def book_delete(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    instance.delete()
    return redirect('books-list')


# Authors
def authors_list(request):
    context = {
        'title': "Список Авторов",
        'author_list': Author.objects.all(),
    }

    return render(request, 'author_list.html', context=context)


def author_create(request):
    form_data = request.POST
    if request.method == 'POST':
        form = AuthorForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('authors-list')
    elif request.method == 'GET':
        form = AuthorForm()

    context = {
        'title': 'Добавить Автора',
        'form': form,
    }
    return render(request, 'author_create.html', context=context)


def author_update(request, pk):
    instance = get_object_or_404(Author, pk=pk)

    form_data = request.POST
    if request.method == 'POST':
        form = AuthorForm(form_data, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('authors-list')
    elif request.method == 'GET':
        form = AuthorForm(instance=instance)

    context = {
        'title': 'Редактиоовать Автора',
        'form': form,
    }
    return render(request, 'author_create.html', context=context)


def author_delete(request, pk):
    instance = get_object_or_404(Author, pk=pk)
    instance.delete()
    return redirect('authors-list')


def logs_mw(request):
    context = {
        'title': 'Логи',
        'logs_mw': Log.objects.all(),
    }
    return render(request, 'logs.html', context=context)


def author_create(request): # noqa :PyCharmTrial
    form_data = request.POST
    if request.method == 'POST':
        form = AuthorForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('authors-list')
    elif request.method == 'GET':
        form = AuthorForm()

    context = {
        'title': 'Добавить Автора',
        'form': form,
    }
    return render(request, 'author_create.html', context=context)


def author_update(request, pk): # noqa :PyCharmTrial
    instance = get_object_or_404(Author, pk=pk)

    form_data = request.POST
    if request.method == 'POST':
        form = AuthorForm(form_data, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('authors-list')
    elif request.method == 'GET':
        form = AuthorForm(instance=instance)

    context = {
        'message': 'Author UPDATE',
        'form': form,
    }
    return render(request, 'author_create.html', context=context)


def author_delete(request, pk): # noqa :PyCharmTrial
    instance = get_object_or_404(Author, pk=pk)
    instance.delete()
    return redirect('authors-list')
