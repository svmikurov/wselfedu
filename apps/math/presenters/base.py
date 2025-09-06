"""Protocols for Math app presenters."""

from typing import TypeVar, Union

from typing_extensions import override
from wse_exercises.core.math import CalcTask

from apps.core.presenters import TaskPresenter
from apps.core.storage.services.iabc import TaskStorageProto
from apps.study.servises.iabc import StrTaskCheckerProto

from ..services.protocol import ExerciseServiceProto
from ..services.types import (
    AssignedCalcAnswerType,
    CalcAnswerType,
    CalcConditionType,
)
from .types import QuestionResponseType, ResultResponseType

AnswerT = TypeVar(
    'AnswerT',
    bound=Union[CalcAnswerType, AssignedCalcAnswerType],
)


class BaseCalcTaskPresenter(
    TaskPresenter[
        CalcConditionType,
        QuestionResponseType,
        AnswerT,
        ResultResponseType,
    ],
):
    """Typed base class for calculation task presenter."""

    def __init__(
        self,
        exercise_service: ExerciseServiceProto[CalcTask],
        task_storage: TaskStorageProto[CalcTask],
        task_checker: StrTaskCheckerProto,
    ) -> None:
        """Construct the presenter."""
        self._exercise_service = exercise_service
        self._task_storage = task_storage
        self._task_checker = task_checker
        self._assignation_id: str | None = None

    @override
    def get_task(self, data: CalcConditionType) -> QuestionResponseType:
        """Get calculation task."""
        task: CalcTask = self._exercise_service.create_task(data)
        uid = self._task_storage.save_task(task)

        return {
            'status': 'success',
            'data': {
                'uid': uid,
                'question': task.question.text,
            },
        }

    @override
    def get_result(
        self,
        data: AnswerT,
    ) -> ResultResponseType:
        """Get user answer checking result."""
        task = self._task_storage.retrieve_task(data['uid'])
        correct_answer = str(task.answer.number)
        user_answer = data['answer']
        # Assigned exercise have assignation ID
        self._assignation_id = data.get('assignation_id')  # type: ignore[assignment]

        is_correct = self._task_checker.check(correct_answer, user_answer)

        payload: ResultResponseType = {
            'status': 'success',
            'data': {
                'is_correct': is_correct,
            },
        }
        if not is_correct:
            payload['data']['correct_answer'] = correct_answer
            payload['data']['user_answer'] = user_answer

        return payload
