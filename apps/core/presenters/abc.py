"""Protocols and ABC for project presenters."""

from abc import ABC, abstractmethod

from typing_extensions import override

from .protocol import (
    AnswerT_contra,
    ConditionT_contra,
    ResultT_co,
    TaskPresenterProto,
    TaskT_co,
)


class TaskPresenter(
    ABC,
    TaskPresenterProto[
        ConditionT_contra,
        TaskT_co,
        AnswerT_contra,
        ResultT_co,
    ],
):
    """Abstract base class for task presenter."""

    @abstractmethod
    @override
    def get_task(self, task_condition: ConditionT_contra) -> TaskT_co:
        """Get task."""

    @abstractmethod
    @override
    def get_result(self, answer_data: AnswerT_contra) -> ResultT_co:
        """Get user answer checking result."""
