from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from books.api.filters import BookFilter, AuthorFilter, CategoryFilter
from books.api.serializers import BookSerializer, AuthorSerializer, CategorySerializer
from books.models import Book, Author, Category
from rest_framework.response import Response
from django.core.cache import cache


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
    # ordering_fields = ['category']
    # filterset_class = CategoryFilter
    permission_classes = ()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        response_data = cache.get(Category.CACHE_OBJECTS_LIST)
        if response_data is not None:
            return Response(response_data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        cache.set(Category.CACHE_OBJECTS_LIST, response_data, 60 * 60 * 24 * 7)  # move to consts

        return Response(response_data)
