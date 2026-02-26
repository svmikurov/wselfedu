"""Calculation exercise assignation views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.contenttypes.models import ContentType
from django.db.models import CharField, IntegerField, OuterRef, Subquery
from django.shortcuts import render
from django.views import generic

from apps.core.views import (
    HtmxDeleteView,
    UserActionKwargsFormMixin,
    UserLoginRequiredMixin,
)
from apps.math.forms import AssignCalculationForm
from apps.math.models import StudentCalculationCondition
from apps.study.models import ExerciseAvailability, ExerciseReward

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.forms import ModelForm
    from django.http import HttpResponse

    from apps.users.models import Person

__all__ = [
    'AssignedCalculationConditionMentorListView',
    'AssignedCalculationConditionMentorCreateView',
    'AssignedCalculationConditionMentorUpdateView',
    'AssignedCalculationConditionMentorDeleteView',
]


class _MentorAssignationQuerySetMixin:
    """Provides mentor's assignations for students.

    Added to edit mode to update the table on success.
    """

    def get_queryset(self) -> QuerySet[StudentCalculationCondition]:
        """Return mentor's assignations for students."""
        content_type = ContentType.objects.get_for_model(
            StudentCalculationCondition
        )

        reward_subquery = ExerciseReward.objects.filter(
            exercise_content_type=content_type,
            exercise_object_id=OuterRef('pk'),
        ).values('amount', 'reward_type')[:1]
        availability_subquery = ExerciseAvailability.objects.filter(
            exercise_content_type=content_type,
            exercise_object_id=OuterRef('pk'),
        ).values('required_count', 'period_type')[:1]

        exercises = (
            StudentCalculationCondition.objects.filter(
                mentorship__mentor=self.user  # type: ignore
            )
            .select_related(
                'mentorship__student',
                'calculation_condition',
            )
            .annotate(
                reward_amount=Subquery(
                    reward_subquery.values('amount')[:1],
                    output_field=IntegerField(),
                ),
                reward_type=Subquery(
                    reward_subquery.values('reward_type')[:1],
                    output_field=CharField(),
                ),
                availability_count=Subquery(
                    availability_subquery.values('required_count')[:1],
                    output_field=IntegerField(),
                ),
                availability_period=Subquery(
                    availability_subquery.values('period_type')[:1],
                    output_field=CharField(),
                ),
            )
        ).order_by('created_at')

        return exercises


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


class AssignedCalculationConditionMentorUpdateView(
    UserLoginRequiredMixin,
    UserActionKwargsFormMixin,
    _MentorAssignationQuerySetMixin,
    generic.UpdateView,  # type: ignore
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

    model = StudentCalculationCondition

    def _get_owner(self) -> Person:
        return self.get_object().mentorship.mentor  # type: ignore[no-any-return]
