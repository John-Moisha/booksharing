from django.urls import reverse


def test_get_form(client):
    url = reverse('contact-us')
    response = client.get(url)
    assert response.status_code == 200


def test_empty_payload(client):
    url = reverse('contact-us')
    response = client.post(url, data={})
    assert response.status_code == 200  # form errors
    assert response.context_data['form'].errors == {
        'full_name': ['This field is required.'],
        'contact_to_email': ['This field is required.'],
        'message': ['This field is required.'],
    }


def test_invalid_payload(client):
    url = reverse('contact-us')
    payload = {
        'full_name': 'Name',
        'contact_to_email': 'email.mail',
        'message': 'Message',
    }
    response = client.post(url, data=payload)
    assert response.status_code == 200  # form errors
    assert response.context_data['form'].errors == {
        'contact_to_email': ['Enter a valid email address.'],
    }


def test_valid_payload(client):
    url = reverse('contact-us')
    payload = {
        'full_name': 'Name',
        'contact_to_email': 'mail@mail.me',
        'message': 'Message',
    }
    response = client.post(url, data=payload, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == [('/', 302)]