from django.urls import reverse
from accounts.models import User


# 1 Sign Up click
def test_get_form(client):
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200


# 2 Empty email
def test_empty_payload(client):
    user = User(is_active=False)
    user.save()

    url = reverse('signup')
    empty_data = {'email': '',
                  'password1': '23456789',
                  'password2': '23456789'}
    response = client.post(url, data=empty_data)

    assert response.status_code == 200  # form errors
    assert response.context_data['form'].errors == {
        'email': ['This field is required.'],
    }


# 3 Invalid payload
def test_invalid_payload(client):
    user = User(is_active=False)
    user.save()

    url = reverse('signup')
    invalid_payload = {'email': 'gmail',
                       'password1': 'password1',
                       'password2': 'password'}
    response = client.post(url, data=invalid_payload)

    assert response.status_code == 200  # form errors
    assert response.context_data['form'].errors == {
        'email': ['Enter a valid email address.'],
        'password2': ['Passwords should match!'],
    }


# 4 Valid payload
def test_valid_payload(client):
    url = reverse('signup')
    valid_payload = {'email': 'example@gmail.com',
                     'password1': 'password',
                     'password2': 'password'}
    response = client.post(url, data=valid_payload, follow=True)

    user = User(is_active=True)
    user.save()

    assert response.status_code == 200
    assert response.redirect_chain == [('/', 302)]
