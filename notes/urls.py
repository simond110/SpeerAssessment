from django.urls import include, path
from rest_framework import routers
from notes.views import NoteViewSet, SearchView

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet, basename="note")
urlpatterns = [
    path('', include(router.urls)),
    path('search', SearchView.as_view(), name="note-search")
]
