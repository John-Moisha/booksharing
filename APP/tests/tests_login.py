from django.urls import reverse
from accounts.models import User


def test_login_success(client):
    url = reverse('login')
    url_check = reverse('my-profile')

    # create user
    password = '12345678'
    email = 'admin-t@me.me'
    avatar = 'avatars/2/2bf448098b7badf3b37e87c510da29bc.jpeg'
    user = User(email=email, username=email, avatar=avatar)
    user.set_password(password)
    user.save()

    # 1 test that client does not have access to url_check resourse
    response = client.get(url_check)
    assert response.status_code == 302

    # 2
    payload = {
        'username': email,
        'password': password,
    }
    response = client.post(url, data=payload)
    assert response.status_code == 302

    # 3
    response = client.get(url_check)
    assert response.status_code == 200
