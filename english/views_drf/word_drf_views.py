"""Django REST framework views."""

from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from english.models import WordModel
from english.serializers import WordSerializer


class IsOwner(permissions.BasePermission):
    """Permission class fo object owner."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Model,
    ) -> bool:
        """Hase user object permission."""
        return obj.user == request.user


class WordListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Word API view."""

    serializer_class = WordSerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> QuerySet:
        """Filter words by current user."""
        return WordModel.objects.filter(user=self.request.user)


class WordRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy Word API View."""

    queryset = WordModel.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsOwner]
