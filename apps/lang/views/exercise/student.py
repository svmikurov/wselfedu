"""Curriculum view."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import generic

from apps.core.views import auth
from apps.lang import models

if TYPE_CHECKING:
    from django.db.models import QuerySet


class ExercisesForTodayView(
    auth.UserLoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Assigned to student exercise list view."""

    template_name = 'lang/exercise/student/index.html'
    context_object_name = 'assignments'
    model = models.EnglishAssignedExercise

    def get_queryset(self) -> QuerySet[models.EnglishAssignedExercise]:
        """Get only current user assigned exercises."""
        return (
            super()
            .get_queryset()
            .filter(mentorship__student=self.user)
            .prefetch_related('mentorship__student')
            .select_related('exercise')
            .order_by('updated_at')
        )
