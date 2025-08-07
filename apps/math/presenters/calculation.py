"""Defines simple calculation exercise presenter."""

from typing import Any

from wse_exercises.core.math import CalcTask

from apps.core.services.iabc import IExerciseService
from apps.core.storage.iabc.itask import ITaskStorage


class CalcPresenter:
    """Calculation task presenter."""

    def __init__(
        self,
        exercise_service: IExerciseService[CalcTask],
        task_storage: ITaskStorage[CalcTask],
    ) -> None:
        """Construct the presenter."""
        self._exercise_service = exercise_service
        self._task_storage = task_storage

    def get_task(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get calculation task."""
        task_dto: CalcTask = self._exercise_service.create_task(data)
        uid = self._task_storage.save_task(task_dto)
        return {
            'uid': uid,
            'question': task_dto.question.text,
        }

    def get_result(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get user answer checking result."""
        task_dto: CalcTask = self._task_storage.retrieve_task(data['uid'])
        is_correct = data['answer'] == str(task_dto.answer.number)
        return {
            'is_correct': is_correct,
            'correct_answer': task_dto.answer.number,
        }
