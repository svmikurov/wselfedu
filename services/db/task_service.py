"""Defines services to save the task to database."""

from django.contrib.contenttypes.models import ContentType
from django.db import models
from wse_exercises.core.math import SimpleCalcTask

from apps.math.models import MathExercise
from apps.math.models.calculation import CalculationTask
from apps.users.models import CustomUser, UserTasks


class TaskDBService:
    """Service to adding the task and task answer to database."""

    # def add_math_task(self, task_dto: SimpleCalcTask) -> None:
    #     """Add math task to database."""
    #     model_type = task_dto, MathExercise
    #     self.add_task(task_dto, model_type)

    def add_task(
        self,
        user: CustomUser,
        task_dto: SimpleCalcTask,
        content_type: models.Model,
    ) -> None:
        """Add task to database."""
        # Get exercise

        exercise = MathExercise.objects.get(name=task_dto.exercise_name)
        content_type = ContentType.objects.get_for_model(MathExercise)

        # Add task

        task_uid = CalculationTask.objects.create(  # type: ignore[attr-defined]
            exercise=exercise,
            operand_1=task_dto.conditions.operand_1,
            operand_2=task_dto.conditions.operand_2,
        )

        # Create user task relationship

        UserTasks.objects.create(
            user=user,
            content_type=content_type,
            object_uid=task_uid.uid,
        )
