import pytest
from django.contrib.auth.models import User
from django.urls import reverse
import json
from model_bakery import baker
from rest_framework.authtoken.models import Token

from utils import is_subset_dict
from notes.models import Note

pytestmark = pytest.mark.django_db


class TestNotesAPI:
    endpoint = reverse("note-list")

    def test_list(self, authenticated_client, auth_user):
        baker.make(Note, owner=auth_user, _quantity=3)

        response = authenticated_client.get(
            self.endpoint
        )
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 3

    def test_list_with_shared_notes(self, authenticated_client, api_client, auth_user):
        note = baker.make(Note, owner=auth_user)
        another_user = baker.make(User, username="other_user")
        another_user.set_password("other_user")
        another_user.save()
        another_user_token, _ = Token.objects.get_or_create(user=another_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {another_user_token}')
        # Get the Notes before sharing notes.
        response = api_client.get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 0
        # Share Note to Another User
        response = authenticated_client.post(reverse('note-share', args=[note.id]), {"username": another_user.username})
        assert response.status_code == 200
        # Get the Nots after being shared
        response = api_client.get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)['results']) == 1

    def test_create(self, authenticated_client, auth_user):
        note = baker.prepare(Note)
        note_data = {
            'title': note.title,
            'content': note.content
        }

        response = authenticated_client.post(
            self.endpoint,
            data=note_data,
            format='json'
        )

        assert response.status_code == 201
        response_data = json.loads(response.content)
        assert is_subset_dict(response_data, note_data)
        assert response_data['owner'] == auth_user.username

    def test_retrieve(self, authenticated_client, auth_user):
        note = baker.make(Note, owner=auth_user)
        note_data = {
            'title': note.title,
            'content': note.content
        }
        url = f'{self.endpoint}{note.id}/'

        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert is_subset_dict(json.loads(response.content), note_data)

    def test_update(self, authenticated_client, auth_user):
        old_item = baker.make(Note, owner=auth_user)
        new_item = baker.prepare(Note)
        item_dict = {
            'title': new_item.title,
            'content': new_item.content
        }

        url = f'{self.endpoint}{old_item.id}/'

        response = authenticated_client.put(
            url,
            item_dict,
            format='json'
        )

        assert response.status_code == 200
        assert is_subset_dict(json.loads(response.content), item_dict)

    @pytest.mark.parametrize('field', ['title', 'content'])
    def test_partial_update(self, field, authenticated_client, auth_user):
        item = baker.make(Note, owner=auth_user)
        item_dict = {
            'title': item.title,
            'content': item.content
        }
        valid_field = item_dict[field]
        url = f'{self.endpoint}{item.id}/'

        response = authenticated_client.patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field

    def test_delete(self, authenticated_client, auth_user):
        item = baker.make(Note, owner=auth_user)
        url = f'{self.endpoint}{item.id}/'

        response = authenticated_client.delete(url)

        assert response.status_code == 204
        assert Note.objects.all().count() == 0

    def test_pagination(self, authenticated_client, auth_user, pagination_page_size):
        baker.make(Note, owner=auth_user, _quantity=pagination_page_size * 2)
        response = authenticated_client.get(
            self.endpoint
        )
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['count'] == pagination_page_size * 2
        assert len(response_data['results']) == pagination_page_size

    def test_note_sharing(self, authenticated_client, auth_user):
        create_test_note = baker.make(Note, owner=auth_user)
        another_user = User.objects.create_user(username='anotheruser', password='password123')
        share_data = {'username': another_user.username}
        response = authenticated_client.post(reverse('note-share', args=[create_test_note.id]), share_data)

        assert response.status_code == 200
        assert another_user in create_test_note.shared_with.all()

    def test_note_sharing_expect_fail_on_other_owner(self, authenticated_client, auth_user):
        other_owner_note = baker.make(Note)
        response = authenticated_client.post(reverse('note-share', args=[other_owner_note.id]), {"username": "test"})
        assert response.status_code == 404


class TestSearchView:
    def test_note_search(self, authenticated_client, dummy_notes):
        response = authenticated_client.get(reverse('note-search'), {'q': 'holiday'})
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data["results"]) == 1
        assert response_data["results"][0]['title'] == 'Holiday Plans'

        response = authenticated_client.get(reverse('note-search'), {'q': 'cake'})
        assert response.status_code == 200

        response_data = response.json()
        assert len(response_data["results"]) == 2
