"""Defines student exercises presenters."""

from django.db.models.query import QuerySet
from typing_extensions import override

from ..models import AssignedExercise, Mentorship
from ..presenters.iabc import StudentExercisesPresenterABC


class StudentExercisesPresenter(StudentExercisesPresenterABC):
    """Student exercises presenter."""

    @staticmethod
    @override
    def get_assigned(
        mentorship: Mentorship | None = None,
    ) -> QuerySet[AssignedExercise]:
        """Get assigned exercises to student by mentor."""
        filters = {}
        if isinstance(mentorship, Mentorship):
            filters['mentorship'] = mentorship

        exercises = AssignedExercise.objects.filter(**filters)
        return exercises
