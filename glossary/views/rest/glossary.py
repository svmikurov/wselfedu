"""Term views."""

from django.db.models import QuerySet
from rest_framework import generics, permissions

from contrib.views.views_rest import IsOwner
from glossary.models import Term, TermCategory
from glossary.serializers import GlossaryCategorySerializer, GlossarySerializer


class GlossaryListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Term API view."""

    queryset = Term.objects.all()
    serializer_class = GlossarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter queryset by current user for response."""
        return Term.objects.filter(user=self.request.user)

    def perform_create(self, serializer: GlossarySerializer) -> None:
        """Add current user to created model instance."""
        serializer.save(user=self.request.user)


class GlossaryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Term term API view."""

    queryset = Term.objects.all()
    serializer_class = GlossarySerializer
    permission_classes = [IsOwner]


class CategoryTermListCreateAPIView(generics.ListCreateAPIView):
    """Create and list Term category API View."""

    serializer_class = GlossaryCategorySerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> None:
        """Get categories only for owner."""
        return TermCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer: GlossaryCategorySerializer) -> None:
        """Add current user to created model instance."""
        serializer.save(user=self.request.user)


class GlossaryCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Term category API view."""

    queryset = TermCategory.objects.all()
    serializer_class = GlossaryCategorySerializer
    permission_classes = [IsOwner]
