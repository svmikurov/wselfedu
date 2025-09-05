"""Defines simple calculation exercise presenter."""

from typing_extensions import override
from wse_exercises.core.math import CalcTask

from apps.core.presenters import TaskPresenter
from apps.core.storage.services.iabc import TaskStorageProtocol
from apps.study.servises.iabc import StrTaskCheckerProtocol

from ..services.protocol import ExerciseServiceProto
from ..services.types import CalcAnswerType, CalcConditionType
from .types import QuestionResponseType, ResultResponseType


class CalculationPresenter(
    TaskPresenter[
        CalcConditionType,
        QuestionResponseType,
        CalcAnswerType,
        ResultResponseType,
    ],
):
    """Calculation task presenter."""

    def __init__(
        self,
        exercise_service: ExerciseServiceProto[CalcTask],
        task_storage: TaskStorageProtocol[CalcTask],
        task_checker: StrTaskCheckerProtocol,
    ) -> None:
        """Construct the presenter."""
        self._exercise_service = exercise_service
        self._task_storage = task_storage
        self._task_checker = task_checker

    @override
    def get_task(self, data: CalcConditionType) -> QuestionResponseType:
        """Get calculation task."""
        task_dto: CalcTask = self._exercise_service.create_task(data)
        uid = self._task_storage.save_task(task_dto)

        return {
            'status': 'success',
            'data': {
                'uid': uid,
                'question': task_dto.question.text,
            },
            # TODO: Fix related data for calculation exercise
            'related_data': {
                'balance': '15',
            },
        }

    @override
    def get_result(self, data: CalcAnswerType) -> ResultResponseType:
        """Get user answer checking result."""
        task_dto: CalcTask = self._task_storage.retrieve_task(data['uid'])
        correct_answer = str(task_dto.answer.number)
        user_answer = data['answer']

        is_correct = self._task_checker.check(correct_answer, user_answer)

        return {
            'status': 'success',
            'data': {
                'is_correct': is_correct,
                'correct_answer': correct_answer,
                'user_answer': '' if is_correct else user_answer,
            },
            # TODO: Fix related data for calculation exercise
            'related_data': {
                'balance': '15',
            },
        }
