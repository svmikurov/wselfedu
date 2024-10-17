"""Django REST framework views."""

from django.db.models.query import QuerySet
from rest_framework import generics, permissions

from contrib.views_rest import IsOwner
from foreign.models import Word
from foreign.serializers import WordSerializer


class WordListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Word API view."""

    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter queryset by current user for response."""
        return Word.objects.filter(user=self.request.user)

    def perform_create(self, serializer: WordSerializer) -> None:
        """Add current user to created model instants."""
        serializer.save(user=self.request.user)


class WordDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy Word API View."""

    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsOwner]
