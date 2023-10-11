import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from model_bakery import baker
from notes.models import Note


@pytest.fixture
def auth_user_pwd():
    return "TestUserPassword"


@pytest.fixture
def auth_user(auth_user_pwd):
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(username="auth_user")
    user.set_password(auth_user_pwd)
    user.save()
    return user


@pytest.fixture
def auth_token(auth_user):
    token, _ = Token.objects.get_or_create(user=auth_user)
    return token.key


@pytest.fixture
def authenticated_client(auth_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
    return client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def pagination_page_size():
    from django.conf import settings
    return settings.REST_FRAMEWORK['PAGE_SIZE']


@pytest.fixture
def dummy_notes(authenticated_client, auth_user):
    example_notes = [
        {
            "title": "Shopping List",
            "content": "1. Apples\n2. Bananas\n3. Milk\n4. Bread\n5. Eggs",
        },
        {
            "title": "Meeting Agenda",
            "content": "1. Introductions\n2. Financials Review\n3. Project Updates\n4. Q&A Session",
        },
        {
            "title": "Holiday Plans",
            "content": "1. Visit Grandma's house\n2. Ski trip to Aspen\n3. New Year's party at Jake's",
        },
        {
            "title": "Books to Read",
            "content": "1. 'Dune' by Frank Herbert\n2. '1984' by George Orwell\n3. 'Moby Dick' by Herman Melville",
        },
        {
            "title": "Daily Routine",
            "content": "1. Morning jog at 6am\n2. Breakfast at 7am\n3. Work from 9am to 5pm\n4. Evening yoga at 7pm",
        },
        {
            "title": "Birthday Party Prep",
            "content": "1. Send out invites\n2. Order cake\n3. Buy decorations\n4. Arrange music playlist",
        },
        {
            "title": "Recipes to Try",
            "content": "1. Spaghetti Carbonara\n2. Veggie Stir-fry\n3. Lemon Drizzle Cake",
        },
        {
            "title": "Garden Tasks",
            "content": "1. Mow the lawn\n2. Plant tomatoes\n3. Water the roses\n4. Buy a new rake",
        },
        {
            "title": "Weekend Getaway",
            "content": "1. Book cabin in the woods\n2. Pack clothes and food\n3. Check weather forecast\n4. Inform neighbors",
        },
        {
            "title": "DIY Projects",
            "content": "1. Build a bookshelf\n2. Repaint the bedroom\n3. Fix the leaky faucet",
        },
        {
            "title": "Movie Watchlist",
            "content": "1. 'Inception'\n2. 'Casablanca'\n3. 'Parasite'\n4. 'Jaws'",
        },
        {
            "title": "Gym Routine",
            "content": "1. Cardio on Mondays\n2. Weightlifting on Wednesdays\n3. Yoga on Fridays",
        },
        {
            "title": "Camping Essentials",
            "content": "1. Tent and pegs\n2. Sleeping bag\n3. Portable stove\n4. First aid kit",
        },
        {
            "title": "Gift Ideas",
            "content": "1. Perfume for Mom\n2. Watch for Dad\n3. Book for Alex\n4. Toy for baby Mia",
        },
        {
            "title": "Daily Affirmations",
            "content": "1. I am strong and capable\n2. Every day brings new opportunities\n3. I believe in myself",
        },
        {
            "title": "Travel Bucket List",
            "content": "1. See the Northern Lights\n2. Visit the Great Wall of China\n3. Trek in the Amazon rainforest",
        },
        {
            "title": "Study Schedule",
            "content": "1. Math - Mondays and Thursdays\n2. History - Tuesdays\n3. Science - Wednesdays and Fridays",
        },
        {
            "title": "Song Playlist",
            "content": "1. 'Imagine' by John Lennon\n2. 'Bohemian Rhapsody' by Queen\n3. 'Smells Like Teen Spirit' by Nirvana",
        },
        {
            "title": "Dream Journal",
            "content": "Had a dream about flying over mountains. Felt a sense of freedom and wonder.",
        },
        {
            "title": "Health Goals",
            "content": "1. Drink 8 glasses of water daily\n2. Walk 10,000 steps a day\n3. Eat more fruits and veggies",
        },
    ]

    # Now you can iterate over example_notes to create instances
    for note in example_notes:
        Note.objects.create(title=note["title"], content=note["content"], owner=auth_user)
