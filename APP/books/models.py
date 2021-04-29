from django.db import models
from books import model_choices as mch
from django.core.cache import cache


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField(null=True)
    date_of_death = models.DateField(null=True)
    country = models.CharField(max_length=64)
    gender = models.BooleanField()
    native_language = models.CharField(max_length=64)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             null=True, default=None)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category = models.CharField(max_length=64)

    CACHE_OBJECTS_LIST = 'CategoryList'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._refresh_cache_objects_list()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._refresh_cache_objects_list()

    @classmethod
    def _refresh_cache_objects_list(cls):
        from books.api.serializers import CategorySerializer  # noqa

        cache.delete(cls.CACHE_OBJECTS_LIST)
        queryset = cls.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        response_data = serializer.data
        cache.set(Category.CACHE_OBJECTS_LIST, response_data, 60 * 60 * 24 * 7)

    def __str__(self):
        return self.name


def book_upload_cover(instance, filename):
    path = f'books/{instance.id}/{filename}'
    return path


# default_cover_none_url = 'books/none/book_none.jpg'
class Book(models.Model):
    title = models.CharField(max_length=128)
    publish_year = models.PositiveSmallIntegerField()
    review = models.CharField(max_length=512)
    condition = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, default=None)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             null=True, default=None)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,
                               null=True, default=None)
    cover = models.FileField(null=True, default=None, upload_to=book_upload_cover)

    def __str__(self):
        return f"{self.id} {self.title} {self.author_id}"


class Log(models.Model):
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=64)
    time = models.PositiveSmallIntegerField()


class RequestBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=mch.REQUEST_STATUSES)
