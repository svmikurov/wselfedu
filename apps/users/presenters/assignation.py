"""Defines student exercises presenters."""

from typing import Any

from django.db.models import F
from django.db.models.query import QuerySet
from typing_extensions import override

from ..models import CustomUser, ExerciseAssigned, Mentorship
from ..presenters.iabc import StudentExercisesPresenterABC


class StudentExercisesPresenter(StudentExercisesPresenterABC):
    """Student exercises presenter."""

    @classmethod
    @override
    def get_assigned_exercise(
        cls,
        mentorship: Mentorship,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by mentor."""
        filters = {
            'mentorship': mentorship,
        }
        return cls._get_exercises(filters)

    @classmethod
    @override
    def get_assigned_exercise_all(
        cls,
        student: CustomUser,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by all his mentors."""
        filters = {
            'mentorship__student': student,
        }
        return cls._get_exercises(filters)

    @staticmethod
    def _get_exercises(
        filters: dict[str, Any],
    ) -> QuerySet[ExerciseAssigned]:
        return (
            ExerciseAssigned.objects.filter(**filters)
            .select_related(
                'mentorship',
                'exercise',
            )
            .prefetch_related(
                'activation_status',
                'exercise_expiration',
                'exercise_task_count',
                'task_award',
            )
            .annotate(count=F('exercise_task_count__count'))
            .annotate(award=F('task_award__award'))
            .annotate(is_daily=F('exercise_expiration__is_daily'))
            .annotate(expiration=F('exercise_expiration__expiration'))
            .annotate(is_active=F('activation_status__is_active'))
        )
