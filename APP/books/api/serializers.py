from rest_framework import serializers

from books.models import Book, Author, Category


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'publish_year',
            'review',
            'condition',
        )


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'date_of_death',
            'country',
            'gender',
            'native_language',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'category',
        )
