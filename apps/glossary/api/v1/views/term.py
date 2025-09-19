"""Term API views."""

from typing import Any

from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.api.permissions import IsOwnerOnly
from apps.core.api.renderers import WrappedJSONRenderer
from apps.glossary.models import Term
from apps.users.models import CustomUser

from ..serializers import TermSerializer


class TermViewSet(viewsets.ModelViewSet[Term]):
    """A viewset for viewing and editing Term instances."""

    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    renderer_classes = [WrappedJSONRenderer]

    def get_queryset(self) -> QuerySet[Term]:
        """Get Term queryset filtered by owner."""
        if isinstance(self.request.user, CustomUser):
            return self.request.user.user_terms.all()  # type: ignore[no-any-return, attr-defined]
        return Term.objects.none()

    def get_renderer_context(self) -> dict[str, Any]:
        """Add message to render context."""
        context = super().get_renderer_context()
        context['message'] = 'User terms'
        return context
