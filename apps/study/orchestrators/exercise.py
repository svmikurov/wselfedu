"""Defense exercise related models management."""

from typing import Any

from django.db import transaction
from typing_extensions import override

from apps.study.models import (
    ExerciseActive,
    ExerciseAssigned,
    ExerciseExpiration,
    ExerciseTaskAward,
    ExerciseTaskCount,
)
from apps.study.orchestrators.iabc import IExerciseAssignator
from apps.users.models import Mentorship


class ExerciseAssignator(IExerciseAssignator):
    """Exercise model management service."""

    def __init__(
        self,
        mentorship: Mentorship,
    ) -> None:
        """Construct the service."""
        self._mentorship = mentorship

    @override
    @transaction.atomic
    def create(self, data: dict[str, Any]) -> ExerciseAssigned:
        """Assign an exercise."""
        assignment = ExerciseAssigned.objects.create(
            mentorship=self._mentorship,
            exercise=data['exercise'],
        )
        self._create_related_objects(assignment, data)
        return assignment

    @staticmethod
    @transaction.atomic
    @override
    def delete(exercise_id: int) -> None:
        """Delete the exercise from assigned exercises."""
        assignment = ExerciseAssigned.objects.get(pk=exercise_id)
        assignment.delete()

    @staticmethod
    def _create_related_objects(
        assignment: ExerciseAssigned,
        data: dict[str, Any],
    ) -> None:
        ExerciseActive.objects.create(
            exercise=assignment, is_active=data['is_active']
        )
        ExerciseExpiration.objects.create(
            exercise=assignment,
            is_daily=data['is_daily'],
            expiration=data['expiration'],
        )
        ExerciseTaskCount.objects.create(
            exercise=assignment, count=data['count']
        )
        ExerciseTaskAward.objects.create(
            exercise=assignment, award=data['award']
        )
