from django_filters import rest_framework as filters

from books.models import Book


class BookFilter(filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['icontains', 'exact'],  # filter(title='awda'), filter(title__exact='awda')
            'condition': ['gt', 'gte', 'lt', 'lte'],
        }