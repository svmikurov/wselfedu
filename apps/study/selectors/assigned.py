"""Defines a selector for retrieving assigned exercise data."""

import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from typing_extensions import override

from apps.math.services.types import CalcConditionType
from apps.users.models import CustomUser

from ..models import ExerciseAssigned
from .iabc import AssignedSelectorABC

logger = logging.getLogger(__name__)


class AssignedSelector(AssignedSelectorABC):
    """Selector for selecting assigned exercise data."""

    @staticmethod
    @override
    def select(
        assignation_id: int,
        exercise_slug: str,
        student: CustomUser,
    ) -> CalcConditionType:
        """Select assigned exercise data."""
        assignation = get_object_or_404(
            ExerciseAssigned,
            pk=assignation_id,
            exercise__slug=exercise_slug,
            mentorship__student=student,
        )

        try:
            exercise_condition = assignation.math_condition_rel.condition

        except (
            ExerciseAssigned.math_condition_rel.RelatedObjectDoesNotExist
        ) as err:
            error_msg = (
                f"Math condition not found for exercise '{exercise_slug}' "
                f'(assignation id: {assignation_id}, '
                f'student id: {student.id}, '
                f'student username: {student.username})'
            )
            logger.error(error_msg)
            raise Http404(error_msg) from err

        else:
            data: CalcConditionType = {
                'exercise_name': assignation.exercise.slug,
                'config': {
                    'min_value': exercise_condition.min_operand,
                    'max_value': exercise_condition.max_operand,
                },
            }
            return data
