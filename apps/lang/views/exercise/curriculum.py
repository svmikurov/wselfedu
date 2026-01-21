"""Curriculum view."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views import generic

from apps.core.views.auth import UserRequestMixin
from apps.lang import models

if TYPE_CHECKING:
    from django.db.models import QuerySet


class ExercisesForTodayView(
    LoginRequiredMixin,
    UserRequestMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Exercise page for today study."""

    template_name = 'lang/exercise/student/index.html'
    context_object_name = 'exercises'
    model = models.EnglishAssignedExercise

    def get_queryset(self) -> QuerySet[models.EnglishAssignedExercise]:
        """Get only current user assigned exercises."""
        return super().get_queryset().filter(mentorship__student=self.user)
