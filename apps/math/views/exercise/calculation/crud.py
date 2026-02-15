"""Stored calculation exercises."""

from django.db.models import QuerySet
from django.views.generic import ListView

from apps.core.views.auth import UserLoginRequiredMixin
from apps.math.models import CalculationCondition


class CalculationListView(
    UserLoginRequiredMixin,
    ListView,  # type: ignore[type-arg]
):
    """User's calculation exercise list view."""

    template_name = 'math/exercise/calculation/stored/list/index.html'
    model = CalculationCondition

    def get_queryset(self) -> QuerySet[CalculationCondition]:
        """Get user's conditions."""
        return super().get_queryset().filter(user=self.user)
