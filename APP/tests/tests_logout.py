from django.urls import reverse
from accounts.models import User


def test_logout_success(client):
    url_login = reverse('login')
    url_logout = reverse('logout')
    url_my_profile = reverse('my-profile')

    # logined user
    password = '12345678'
    email = 'admin-t@me.me'
    avatar = 'avatars/2/2bf448098b7badf3b37e87c510da29bc.jpeg'
    user = User(email=email, username=email, avatar=avatar)
    user.set_password(password)
    user.save()
    payload = {
        'username': email,
        'password': password,
    }
    client.post(url_login, data=payload)

    # 1 Chek that User is login
    response = client.get(url_my_profile)
    assert response.status_code == 200

    # 2 Logout button
    response = client.get(url_logout)
    assert response.status_code == 200

    # 3 User is logout
    client.post(url_logout)
    response = client.get(url_my_profile)
    assert response.status_code == 302
