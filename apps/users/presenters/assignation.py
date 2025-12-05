"""Defines student exercises presenters."""

from typing import Any

from django.db.models import F
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from typing_extensions import override

from apps.study.models import ExerciseAssigned

from ..models import Mentorship, Person
from ..presenters.iabc import StudentExercisesPresenterABC


class StudentExercisesPresenter(StudentExercisesPresenterABC):
    """Student exercises presenter."""

    @classmethod
    @override
    def get_assigned_by_mentor(
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
    def get_assigned_all(
        cls,
        student: Person,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by all his mentors."""
        filters = {
            'mentorship__student': student,
        }
        return cls._get_exercises(filters)

    @classmethod
    @override
    def get_exercise_meta(
        cls,
        assignation_id: int,
        student: Person,
    ) -> ExerciseAssigned:
        """Get assigned exercise meta data."""
        obj = get_object_or_404(
            ExerciseAssigned.objects,
            pk=assignation_id,
            mentorship__student=student,
        )
        return obj

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
