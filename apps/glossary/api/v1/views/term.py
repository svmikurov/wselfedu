"""Term API views."""

from typing import Any

from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.api.permissions import IsOwnerOnly
from apps.core.api.renderers import WrappedJSONRenderer
from apps.glossary.models import Term
from apps.users.models import Person

from ..serializers import TermSerializer


@extend_schema_view(
    list=extend_schema(
        summary='Get a terms',
        tags=['Glossary'],
    ),
    retrieve=extend_schema(
        summary='Get specific term',
        tags=['Glossary'],
    ),
    create=extend_schema(
        summary='Crate term',
        tags=['Glossary'],
    ),
    update=extend_schema(
        summary='Update term',
        tags=['Glossary'],
    ),
    partial_update=extend_schema(
        summary='Partially update the term',
        tags=['Glossary'],
    ),
    destroy=extend_schema(
        summary='Delete term',
        tags=['Glossary'],
    ),
)
class TermViewSet(viewsets.ModelViewSet[Term]):
    """A viewset for viewing and editing Term instances."""

    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]
    renderer_classes = [WrappedJSONRenderer]

    def get_queryset(self) -> QuerySet[Term]:  # type: ignore[override]
        """Get Term queryset filtered by owner."""
        if isinstance(self.request.user, Person):
            return self.request.user.user_terms.all()
        return Term.objects.none()

    def get_renderer_context(self) -> dict[str, Any]:
        """Add message to render context."""
        context = super().get_renderer_context()
        context['message'] = 'User terms'
        return context
