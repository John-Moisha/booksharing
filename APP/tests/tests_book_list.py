from django.urls import reverse
from books.models import Author, Book
from accounts.models import User
from faker import Faker
from datetime import datetime
import random


# author create
def create_author():
    fake = Faker()

    first_name = fake.first_name()
    last_name = fake.last_name()
    country = fake.country()
    date_of_birth = fake.date()
    date_of_death = fake.date()
    gender = bool(random.getrandbits(1))
    native_language = fake.country_code()

    author = Author(first_name=first_name,
                    last_name=last_name,
                    country=country,
                    date_of_birth=date_of_birth,
                    date_of_death=date_of_death,
                    gender=gender,
                    native_language=native_language)
    author.save()
    return author


# book create
def create_book(client):
    fake = Faker()

    author = create_author()
    title = fake.word().capitalize()
    publish_year = random.randint(0, datetime.now().year)
    review = fake.text()
    condition = random.randint(1, 5)

    book = Book(author=author,
                title=title,
                publish_year=publish_year,
                review=review,
                condition=condition,
                user=client)
    book.save()
    return book


def test_get_form(client):
    url = reverse('books:books-list')
    response = client.get(url)
    assert response.status_code == 200


def test_get_books_list_for_login_user(client):
    login_url = reverse('login')
    url_logout = reverse('logout')
    book_list_url = reverse('books:books-list')
    create_book_url = reverse('books:book-create')

    # create some books from other people
    user = None
    create_book(user)
    create_book(user)

    # create user
    password = '12345678'
    email = 'admin-t@me.me'
    login_user = User(email=email, username=email)
    login_user.set_password(password)
    login_user.save()

    # login user
    payload = {
        'username': email,
        'password': password,
    }
    client.post(login_url, data=payload)
    create_book(login_user)

    # add book from login user
    fake = Faker()

    author = create_author()
    title = fake.word().capitalize()
    publish_year = random.randint(0, datetime.now().year)
    review = fake.text()
    condition = random.randint(1, 5)
    payload = {"author": author,
               "title": title,
               "publish year": publish_year,
               "review": review,
               "condition": condition,
               "coverage": 'books/154/IMG_20210320_000433.jpg'}
    client.put(create_book_url, data=payload)

    # books list for login user
    queryset_for_login_user = Book.objects.exclude(user=login_user)
    response = client.get(book_list_url)
    assert str(response.context_data['book_list']) == str(queryset_for_login_user)
    assert response.status_code == 200

    # books list for anonym user
    queryset_for_anonym = Book.objects.all()
    client.get(url_logout)
    response = client.get(book_list_url)
    assert str(response.context_data['object_list']) == str(queryset_for_anonym)
    assert response.status_code == 200
