"""Django REST framework views."""

from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from foreign.models import Word
from foreign.serializers import WordSerializer


class IsOwner(permissions.BasePermission):
    """Permission class fo object owner."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Model,
    ) -> bool:
        """Has current user the permission to the model instance."""
        return obj.user == request.user


class WordListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Word API view."""

    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter words by current user for response."""
        return Word.objects.filter(user=self.request.user)

    def perform_create(self, serializer: WordSerializer) -> None:
        """Add current user to created model instants."""
        serializer.save(user=self.request.user)


class WordDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy Word API View."""

    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsOwner]
