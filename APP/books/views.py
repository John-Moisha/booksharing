from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView,
    TemplateView, View, DetailView)
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from books.utils import display
from books.forms import BookForm, AuthorForm
from books.models import Book, Author, Log, RequestBook
from books import model_choices as mch
import csv
import xlwt


class FormUserKwargMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class Index(TemplateView):
    template_name = 'index.html'


# Books List
class BookList(ListView):
    template_name = 'books/books_list.html'
    queryset = Book.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if str(self.request.user.__class__) == "<class 'accounts.models.User'>":
            return queryset.exclude(user=self.request.user)
        else:
            return queryset
        # return queryset.exclude(user=self.request.user)


# MyBook List
class MyBookList(LoginRequiredMixin, ListView):
    template_name = 'books/my_books_list.html'
    queryset = Book.objects.all().select_related('author')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


# My Requested Books
class MyRequestedBooks(LoginRequiredMixin, ListView):
    queryset = RequestBook.objects.all()
    template_name = 'books/requestbooks_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(recipient=self.request.user)


# Requested Books
class RequestedBooks(LoginRequiredMixin, ListView):
    queryset = RequestBook.objects.all()
    template_name = 'books/requested_books_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(book__user=self.request.user)


# Create Request Book
class RequestBookCreate(LoginRequiredMixin, View):

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        if not RequestBook.objects.filter(book=book, recipient=request.user).exists():
            RequestBook.objects.create(book=book, recipient=request.user, status=mch.STATUS_IN_PROGRESS)
        return redirect('books:books-list')


class _ChangeRequestBaseView(LoginRequiredMixin, View):
    CURRENT_STATUS = None
    NEW_STATUS = None
    REDIRECT_NAME = None
    MESSAGE = None

    def get(self, request, request_id):
        request_obj = get_object_or_404(RequestBook, pk=request_id, status=self.CURRENT_STATUS)
        request_obj.status = self.NEW_STATUS
        request_obj.save(update_fields=('status',))

        if self.MESSAGE:
            messages.add_message(request, messages.INFO, self.MESSAGE)

        return redirect(self.REDIRECT_NAME)


class RequestBookConfirm(_ChangeRequestBaseView):
    CURRENT_STATUS = mch.STATUS_IN_PROGRESS
    NEW_STATUS = mch.STATUS_CONFIRMED
    REDIRECT_NAME = 'books:requested-books'
    MESSAGE = 'Book Request Was Confirmed!'


class RequestBookReject(_ChangeRequestBaseView):
    CURRENT_STATUS = mch.STATUS_IN_PROGRESS
    NEW_STATUS = mch.STATUS_REJECT
    REDIRECT_NAME = 'books:requested-books'
    MESSAGE = 'Book Request Was Rejected!'


class RequestBookSentViaEmail(_ChangeRequestBaseView):
    CURRENT_STATUS = mch.STATUS_CONFIRMED
    NEW_STATUS = mch.STATUS_SENT_TO_RECIPIENT
    REDIRECT_NAME = 'books:requested-books'


class RequestBookReceivedBook(_ChangeRequestBaseView):
    CURRENT_STATUS = mch.STATUS_SENT_TO_RECIPIENT
    NEW_STATUS = mch.STATUS_RECIPIENT_RECEIVED_BOOK
    REDIRECT_NAME = 'books:my-requested-books'


class RequestBookSentBackToOwner(_ChangeRequestBaseView):
    CURRENT_STATUS = mch.STATUS_RECIPIENT_RECEIVED_BOOK
    NEW_STATUS = mch.STATUS_SENT_BACK_TO_OWNER
    REDIRECT_NAME = 'books:my-requested-books'


class RequestBookOwnerReceivedBack(_ChangeRequestBaseView):
    CURRENT_STATUS = mch.STATUS_SENT_BACK_TO_OWNER
    NEW_STATUS = mch.STATUS_OWNER_RECEIVED_BACK
    REDIRECT_NAME = 'books:requested-books'


class BookCreate(FormUserKwargMixin, CreateView):
    model = Book
    success_url = reverse_lazy('books:my-books-list')
    form_class = BookForm

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'Book Was Created')

        return super().get_success_url()


class BookUpdate(FormUserKwargMixin, UpdateView):
    model = Book
    success_url = reverse_lazy('books:books-list')
    form_class = BookForm

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'Book Was Updated')

        return super().get_success_url()


class BookView(FormUserKwargMixin, DetailView):
    model = Book
    template_name = 'books/book_view.html'


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books:books-list')

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'Book Was Deleted')

        return super().get_success_url()


# Authors List
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
    success_url = reverse_lazy('books:my-authors-list')
    form_class = AuthorForm

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'Author Was Created')

        return super().get_success_url()


class AuthorUpdate(FormUserKwargMixin, UpdateView):
    model = Author
    success_url = reverse_lazy('books:authors-list')
    form_class = AuthorForm

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'Author Was Updated')

        return super().get_success_url()


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('books:authors-list')

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'Author Was Deleted')

        return super().get_success_url()


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
