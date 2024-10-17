"""Glossary views."""

from django.db.models import QuerySet
from rest_framework import generics, permissions

from contrib.views_rest import IsOwner
from glossary.models import Glossary
from glossary.serializers import GlossarySerializer


class GlossaryListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter queryset by current user for response."""
        return Glossary.objects.filter(user=self.request.user)

    def perform_create(self, serializer: GlossarySerializer) -> None:
        """Add current user to created model instants."""
        serializer.save(user=self.request.user)


class GlossaryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
    permission_classes = [IsOwner]
