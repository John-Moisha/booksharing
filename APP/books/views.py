import csv
import xlwt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView,
    TemplateView, View
)
from django.http import HttpResponse
from books.utils import display

from books.forms import BookForm, AuthorForm
from books.models import Book, Author, Log


class FormUserKwargMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class Index(TemplateView):
    template_name = 'index.html'

#Books List
class BookList(ListView):
    template_name = 'books/books_list.html'
    queryset = Book.objects.all()

# MyBook
class MyBookList(LoginRequiredMixin, ListView):
    template_name = 'books/my_books_list.html'
    queryset = Book.objects.all().select_related('author')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class BookCreate(FormUserKwargMixin, CreateView):
    model = Book
    success_url = reverse_lazy('books:books-list')
    form_class = BookForm


class BookUpdate(FormUserKwargMixin, UpdateView):
    model = Book
    success_url = reverse_lazy('books:book-list')
    form_class = BookForm


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books:books-list')

#Authors List
class AuthorList(ListView):
    template_name = 'books/authors_list.html'
    queryset = Author.objects.all()


# My Authors
class MyAuthorList(ListView):
    template_name = 'books/my_authors_list.html'
    queryset = Author.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class AuthorCreate(FormUserKwargMixin, CreateView):
    model = Author
    success_url = reverse_lazy('books:authors-list')
    form_class = AuthorForm


class AuthorUpdate(FormUserKwargMixin, UpdateView):
    model = Author
    success_url = reverse_lazy('books:authors-list')
    form_class = AuthorForm


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('books:authors-list')


# log
class LogsMW(ListView):
    template_name = 'logs.html'
    queryset = Log.objects.all()


# CSV Download Books list
class DownloadCSVBooksView(View):

    HEADERS = (
        'id',
        'title',
        'author.full_name',
        'author.get_full_name',
        'publish_year',
        'condition',
    )

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books_list.csv"'

        writer = csv.writer(response, delimiter=';')

        writer.writerow(self.HEADERS)

        for book in Book.objects.all().select_related('author').iterator():
            writer.writerow([
                display(book, header)
                for header in self.HEADERS
            ])

        return response


# XLSX Download Book list
class DownloadXLSXBooksView(View):

    HEADERS = (
        'id',
        'title',
        'author.full_name',
        'author.get_full_name',
        'publish_year',
        'condition',
    )

    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="books_list.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(self.HEADERS)):
            ws.write(row_num, col_num, self.HEADERS[col_num], font_style)

        font_style = xlwt.XFStyle()

        for book in Book.objects.all().select_related('author').iterator():
            row_num = row_num + 1
            for col_num in range(len(self.HEADERS)):
                ws.write(row_num, col_num, display(book, self.HEADERS[col_num]), font_style)

        wb.save(response)
        return response


# CSV Download Authors list
class DownloadCSVAuthorsView(View):

    HEADERS = (
        'id',
        'full_name',
        'date_of_birth',
        'date_of_death',
        'country',
        'gender',
        'native_language',
    )

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="authors_list.csv"'

        writer = csv.writer(response, delimiter=';')

        writer.writerow(self.HEADERS)

        for author in Author.objects.all().iterator():
            writer.writerow([
                display(author, header)
                for header in self.HEADERS
            ])

        return response


# XLSX Authors
class DownloadXLSXAuthorsView(View):

    HEADERS = (
        'id',
        'full_name',
        'date_of_birth',
        'date_of_death',
        'country',
        'gender',
        'native_language',
    )

    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="authors_list.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(self.HEADERS)):
            ws.write(row_num, col_num, self.HEADERS[col_num], font_style)

        font_style = xlwt.XFStyle()

        for author in Author.objects.all().iterator():
            row_num = row_num + 1
            for col_num in range(len(self.HEADERS)):
                ws.write(row_num, col_num, display(author, self.HEADERS[col_num]), font_style)

        wb.save(response)
        return response
