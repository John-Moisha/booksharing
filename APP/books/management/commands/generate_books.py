from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime
from books.models import Book


class Command(BaseCommand):
    help = 'Generate Random Books Data'  # noqa

    def add_arguments(self, parser):
        parser.add_argument('quant', type=int, default=0)

    def handle(self, *args, **options):
        fake = Faker()
        books_list = []

        for _ in range(options['quant']):
            author = fake.name()
            title = fake.word().capitalize()
            publish_year = random.randint(0, datetime.now().year)
            review = fake.text()
            condition = random.randint(1, 5)

            books_list.append(Book(
                author=author,
                title=title,
                publish_year=publish_year,
                review=review,
                condition=condition
            ))
        Book.objects.bulk_create(books_list)
