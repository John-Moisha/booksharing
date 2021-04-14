from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from books.api.filters import BookFilter, AuthorFilter, CategoryFilter
from books.api.serializers import BookSerializer, AuthorSerializer, CategorySerializer
from books.models import Book, Author, Category


class BookModelViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['condition', 'title']
    filterset_class = BookFilter


class AuthorModelViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['first_name']
    filterset_class = AuthorFilter


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['category']
    filterset_class = CategoryFilter
