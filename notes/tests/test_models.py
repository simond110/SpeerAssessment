import pytest
from django.contrib.auth.models import User
from notes.models import Note


@pytest.mark.django_db
def test_note_creation():
    user = User.objects.create(username='testuser', password='password123')
    note = Note.objects.create(title='Test Note', content='This is a test content.', owner=user)

    assert Note.objects.count() == 1
    assert note.title == 'Test Note'
