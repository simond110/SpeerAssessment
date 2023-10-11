import pytest
from django.contrib.auth.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestAuthAPI:
    def test_user_signup(self, api_client):
        user_data = {'username': 'test-sign-up', 'password': 'password123', 'retype_password': "password123",
                     "email": "test.signup@test.com", "first_name": "first name", "last_name": "last name"}
        response = api_client.post(reverse('user-signup'),
                                   user_data)  # Adjust 'user-signup' with the correct URL pattern name

        assert response.status_code == 201
        assert User.objects.count() == 1

    def test_user_login(self, api_client, auth_user, auth_user_pwd):
        login_data = {'username': auth_user.username, 'password': auth_user_pwd}
        response = api_client.post(reverse('api-token-auth'),
                                   login_data)
        assert response.status_code == 200
        assert 'token' in response.data

    def test_user_login_expected_fail(self, api_client, auth_user, auth_user_pwd):
        login_data = {'username': auth_user.username, 'password': auth_user_pwd + "wrong pwd"}
        response = api_client.post(reverse('api-token-auth'),
                                   login_data)

        assert response.status_code == 400
