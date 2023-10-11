from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from rest_framework import viewsets, mixins, status, generics
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        current_action = self.action
        if current_action == "list" or current_action == "retrieve":
            # Return a queryset based on authenticated user including shared notes
            return Note.objects.filter(Q(owner=self.request.user) | Q(shared_with=self.request.user))
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        note = self.get_object()

        # Fetch the user to share the note with
        username = request.data.get('username')
        try:
            user_to_share = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        if user_to_share != request.user:
            note.shared_with.add(user_to_share)
            note.save()

        return Response({"success": f"Note shared with {username}!"})


class SearchView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query is None:
            return Note.objects.filter(Q(owner=self.request.user) | Q(shared_with=self.request.user))
        Note.objects.update(search_vector=SearchVector('title', 'content'))
        return Note.objects.filter(Q(owner=self.request.user) | Q(shared_with=self.request.user)).filter(
            search_vector=SearchQuery(query))
