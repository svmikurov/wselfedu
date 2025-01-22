"""Term views."""

from django.db.models import QuerySet
from rest_framework import generics, permissions

from contrib.views.views_rest import IsOwner
from glossary.models import Term, TermCategory
from glossary.serializers import TermCategorySerializer, TermSerializer


class TermListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Term API view."""

    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter queryset by current user for response."""
        return Term.objects.filter(user=self.request.user).order_by('-pk')

    def perform_create(self, serializer: TermSerializer) -> None:
        """Add current user to created model instance."""
        serializer.save(user=self.request.user)


class TermDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy term API view."""

    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [IsOwner]


class CategoryTermListCreateAPIView(generics.ListCreateAPIView):
    """Create and list Term category API View."""

    serializer_class = TermCategorySerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> QuerySet[TermCategory, TermCategory]:
        """Get categories only for owner."""
        return TermCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer: TermCategorySerializer) -> None:
        """Add current user to created model instance."""
        serializer.save(user=self.request.user)


class CategoryTermDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Term category API view."""

    queryset = TermCategory.objects.all()
    serializer_class = TermCategorySerializer
    permission_classes = [IsOwner]
