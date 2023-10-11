import pytest
from django.contrib.auth.models import User
from notes.models import Note
from notes.serializers import NoteSerializer


@pytest.mark.django_db
def test_note_serializer():
    user = User.objects.create(username='testuser', password='password123')
    note = Note.objects.create(title='Test Note', content='This is a test content.', owner=user)
    serializer = NoteSerializer(note)

    assert serializer.data['title'] == 'Test Note'
    assert serializer.data['content'] == 'This is a test content.'


@pytest.mark.django_db
def test_note_serializer_reverse(auth_user):
    data = {'title': 'Test Note', 'content': 'This is a test content.'}
    serializer = NoteSerializer(data=data)
    assert serializer.is_valid()
    note = serializer.save(owner=auth_user)

    assert note.title == 'Test Note'
    assert note.content == 'This is a test content.'
    assert note.owner == auth_user
