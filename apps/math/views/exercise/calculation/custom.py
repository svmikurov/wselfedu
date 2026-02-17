"""Stored calculation exercises."""

from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView

from apps.core.views import (
    BaseCreateView,
    BaseUpdateView,
    HtmxOwnerDeleteView,
    HtmxResponseFormMixin,
    UserLoginRequiredMixin,
)
from apps.math.forms import (
    CreateCalculationConditionsForm,
    UpdateCalculationConditionsForm,
)
from apps.math.models import CalculationCondition


class CalculationListView(
    UserLoginRequiredMixin,
    ListView,  # type: ignore[type-arg]
):
    """User's calculation exercise list view."""

    template_name = 'math/exercise/calculation/custom/index.html'
    context_object_name = 'exercises'
    paginate_by = 15
    model = CalculationCondition

    def get_queryset(self) -> QuerySet[CalculationCondition]:
        """Get user's conditions."""
        return super().get_queryset().filter(user=self.user)


class CalculationCreateView(HtmxResponseFormMixin, BaseCreateView):
    """Create calculation view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('math:regular_calculation_exercise_list')
    form_class = CreateCalculationConditionsForm


class CalculationUpdateView(
    HtmxResponseFormMixin,
    BaseUpdateView[CalculationCondition],
):
    """Calculation exercise update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('math:regular_calculation_exercise_list')
    form_class = UpdateCalculationConditionsForm
    model = CalculationCondition


class CalculationDeleteView(HtmxOwnerDeleteView):
    """Calculation exercise delete view."""

    model = CalculationCondition
