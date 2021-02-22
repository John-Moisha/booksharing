from django.core.management.base import BaseCommand
from faker import Faker
import random
from books.models import Author


class Command(BaseCommand):
    help = 'Generate Random Authors Data'  # noqa

    def add_arguments(self, parser):
        parser.add_argument('quant', type=int, default=0)

    def handle(self, *args, **options):
        fake = Faker()
        authors_list = []

        for _ in range(options['quant']):
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            date_of_birth = '2020-10-10',
            date_of_death = '2021-10-10',
            country = fake.country(),
            gender = random.choice([True, False]),
            native_language = fake.country_code()

            authors_list.append(Author(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                date_of_death=date_of_death,
                country=country,
                gender=gender,
                native_language=native_language
            ))
        Author.objects.bulk_create(authors_list)

