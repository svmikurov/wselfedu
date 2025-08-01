"""Defines database service for simple calculation exercise."""

import uuid

from django.db import models
from wse_exercises.core import MathEnum
from wse_exercises.core.math import SimpleCalcTask
from wse_exercises.core.math.rest import SimpleCalcResult

from apps.math.models.simple import SimpleTask
from apps.users.models import CustomUser


class SimpleCalcDBService:
    """Database service for simple calculation exercise."""

    def __init__(
        self,
        manager: models.Manager[SimpleTask],
    ) -> None:
        """Construct the service."""
        self._manager = manager

    def save(
        self,
        user: CustomUser,
        task_dto: SimpleCalcTask,
        user_answer: int,
        response_dto: SimpleCalcResult,
    ) -> uuid.UUID:
        """Save the task to database."""
        return self._manager.create(
            user=user,
            exercise_name=task_dto.exercise_name,
            operand_1=self._get_first_operand(task_dto),
            operand_2=task_dto.conditions.operand_2,
            created_at=task_dto.created_at,
            user_answer=user_answer,
            is_correct=response_dto.is_correct,
            checked_at=response_dto.checked_at,
        ).uid

    def save_rewardable(
        self,
        user: CustomUser,
        task_dto: SimpleCalcTask,
    ) -> uuid.UUID:
        """Save the created rewardable task to database."""

    def result_rewardable(
        self,
        uid: uuid.UUID,
        task_dto: SimpleCalcTask,
    ) -> None:
        """Save the result of rewardable task to database."""

    @staticmethod
    def _get_first_operand(task_dto: SimpleCalcTask) -> int:
        # In the division exercise, the divisor is calculated as
        # the multiplication of the first operand by the second.
        operand_1 = task_dto.conditions.operand_1
        if task_dto.exercise_name == MathEnum.DIVISION:
            return operand_1 * task_dto.conditions.operand_2
        return operand_1
