"""Protocols and ABC for project presenters."""

from typing import Protocol, TypeVar

ConditionT_contra = TypeVar('ConditionT_contra', contravariant=True)
TaskT_co = TypeVar('TaskT_co', covariant=True)
AnswerT_contra = TypeVar('AnswerT_contra', contravariant=True)
ResultT_co = TypeVar('ResultT_co', covariant=True)


class TaskPresenterProto(
    Protocol[
        ConditionT_contra,
        TaskT_co,
        AnswerT_contra,
        ResultT_co,
    ],
):
    """Protocol for task presenter interface."""

    def get_task(self, task_condition: ConditionT_contra) -> TaskT_co:
        """Get task."""

    def get_result(self, answer_data: AnswerT_contra) -> ResultT_co:
        """Get user answer checking result."""
