"""Defines student exercises presenters."""

from django.db.models import F
from django.db.models.query import QuerySet
from typing_extensions import override

from ..models import ExerciseAssigned, Mentorship
from ..presenters.iabc import StudentExercisesPresenterABC


class StudentExercisesPresenter(StudentExercisesPresenterABC):
    """Student exercises presenter."""

    @staticmethod
    @override
    def get_assigned_exercise(
        mentorship: Mentorship | None = None,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by mentor."""
        filters = {}
        if isinstance(mentorship, Mentorship):
            filters['mentorship'] = mentorship

        exercises = (
            ExerciseAssigned.objects.filter(**filters)
            .select_related(
                'mentorship',
                'exercise',
            )
            .annotate(count=F('exercise_task_count__count'))
            .annotate(award=F('task_award__award'))
            .annotate(is_daily=F('exercise_expiration__is_daily'))
            .annotate(expiration=F('exercise_expiration__expiration'))
            .annotate(is_active=F('activation_status__is_active'))
        )
        return exercises
