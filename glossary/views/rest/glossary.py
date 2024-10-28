"""Glossary views."""

from django.db.models import QuerySet
from rest_framework import generics, permissions

from contrib.views_rest import IsOwner
from glossary.models import Glossary, GlossaryCategory
from glossary.serializers import GlossaryCategorySerializer, GlossarySerializer


class GlossaryListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter queryset by current user for response."""
        return Glossary.objects.filter(user=self.request.user)

    def perform_create(self, serializer: GlossarySerializer) -> None:
        """Add current user to created model instance."""
        serializer.save(user=self.request.user)


class GlossaryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Glossary term API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
    permission_classes = [IsOwner]


class CategoryTermListCreateAPIView(generics.ListCreateAPIView):
    """Create and list Glossary category API View."""

    serializer_class = GlossaryCategorySerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> None:
        """Get categories only for owner."""
        return GlossaryCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer: GlossaryCategorySerializer) -> None:
        """Add current user to created model instance."""
        serializer.save(user=self.request.user)


class GlossaryCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Glossary category API view."""

    queryset = GlossaryCategory.objects.all()
    serializer_class = GlossaryCategorySerializer
    permission_classes = [IsOwner]
