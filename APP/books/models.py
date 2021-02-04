from django.db import models


# Create your models here.
class Book(models.Model):
    author = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    publish_year = models.PositiveSmallIntegerField()
    review = models.CharField(max_length=512)
    condition = models.PositiveSmallIntegerField()


# Author` с полями: first_name, last_name, date_of_birth,
# date_of_death, country, gender, native_language
class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    date_of_death = models.DateField()
    country = models.CharField(max_length=64)
    gender = models.BooleanField()
    native_language = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        # args - tuple
        # kwargs - dict
        # print('START SAVE')
        # self.first_name = self.first_name.capitalize()
        # self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)
        # print('END SAVE')

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super().save(
    #         force_insert=force_insert, force_update=force_update, using=using,
    #         update_fields=update_fields
    #     )