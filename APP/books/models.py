from django.db import models


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


class Category(models.Model):
    category = models.CharField(max_length=64)


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


class Log(models.Model):
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=64)
    time = models.PositiveSmallIntegerField()
