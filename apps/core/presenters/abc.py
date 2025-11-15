"""Protocols and ABC for project presenters."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from apps.users.models import CustomUser

from .protocol import (
    AnswerT_contra,
    ConditionT_contra,
    ResultT_co,
    TaskPresenterProto,
    TaskT_co,
)

T = TypeVar('T')
T_contra = TypeVar('T_contra', contravariant=True)


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


class StudyPresenterGenABC(ABC, Generic[T_contra, T]):
    """ABC for item study via presentation."""

    @abstractmethod
    def get_presentation_case(
        self,
        user: CustomUser,
        presentation_params: T_contra,
    ) -> T:
        """Get item study presentation case."""
