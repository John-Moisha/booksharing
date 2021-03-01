from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime
from books.models import Book, Author, Category


class Command(BaseCommand):
    help = 'Generate Random Books Authors Data'  # noqa

    def add_arguments(self, parser):
        parser.add_argument('quant', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        authors = []

        for _ in range(options['quant']):
            first_name = fake.first_name().capitalize()
            last_name = fake.last_name().capitalize()
            date_of_birth = fake.date()
            date_of_death = fake.date()
            country = fake.country()
            gender = bool(random.getrandbits(1))
            native_language = fake.country_code()
            authors.append(Author(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                date_of_death=date_of_death,
                country=country,
                gender=gender,
                native_language=native_language
            ))
        Author.objects.bulk_create(authors)

        books_list = []
        for _ in range(options['quant']):
            author = Author.objects.order_by('?').last()
            title = fake.word()
            category = random.choice(Category.objects.all())
            publish_year = random.randint(0, datetime.now().year)
            review = fake.text()
            condition = random.randint(1, 5)
            books_list.append(Book(
                author=author,
                title=title,
                category=category,
                publish_year=publish_year,
                review=review,
                condition=condition,
            ))
        Book.objects.bulk_create(books_list)
