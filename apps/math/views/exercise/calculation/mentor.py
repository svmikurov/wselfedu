"""Calculation exercise assignation views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views import generic

from apps.core.views import (
    HtmxDeleteView,
    UserActionKwargsFormMixin,
    UserLoginRequiredMixin,
)
from apps.math.forms import AssignCalculationForm
from apps.math.models import AssignedCalculationCondition

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.forms import ModelForm
    from django.http import HttpResponse

    from apps.users.models import Person

__all__ = [
    'AssignedCalculationConditionMentorListView',
    'AssignedCalculationConditionMentorCreateView',
    'AssignedCalculationConditionMentorDeleteView',
]


class _MentorAssignationQuerySetMixin:
    """Provides mentor's assignations for students."""

    def get_queryset(self) -> QuerySet[AssignedCalculationCondition]:
        """Return mentor's assignations for students."""
        return AssignedCalculationCondition.objects.filter(
            mentorship__mentor=self.user  # type: ignore
        ).select_related(
            'mentorship__student',
            'calculation_condition',
        )


class AssignedCalculationConditionMentorListView(
    UserLoginRequiredMixin,
    _MentorAssignationQuerySetMixin,
    generic.ListView,  # type: ignore
):
    """Assigned to student calculation list."""

    template_name = 'math/exercise/calculation/mentor/index.html'
    context_object_name = 'exercises'


class AssignedCalculationConditionMentorCreateView(
    UserLoginRequiredMixin,
    UserActionKwargsFormMixin,
    _MentorAssignationQuerySetMixin,
    generic.CreateView,  # type: ignore
):
    """Create assignation for student.

    Renders partial template for HTMX.
    """

    template_name = 'components/crispy_form.html'
    form_class = AssignCalculationForm

    def form_valid(self, form: ModelForm) -> HttpResponse:  # type: ignore
        """Save assignation and return updated table."""
        form.save()
        return render(
            self.request,
            'math/exercise/calculation/mentor/_table.html',
            {'exercises': self.get_queryset()},
        )


class AssignedCalculationConditionMentorDeleteView(HtmxDeleteView):
    """Delete by mentor assignation of calculation exercise."""

    model = AssignedCalculationCondition

    def _get_owner(self) -> Person:
        return self.get_object().mentorship.mentor  # type: ignore[no-any-return]
