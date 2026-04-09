"""Protocol for exercise domain dependencies."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import TaskBuilderProtocol

ConfT = TypeVar('ConfT', contravariant=True)
CaseT = TypeVar('CaseT', contravariant=True)
TaskT = TypeVar('TaskT', covariant=True)


class AbstractTaskBuilder(
    ABC,
    TaskBuilderProtocol[ConfT, CaseT, TaskT],
):
    """Protocol cor Exercise task builder interface."""

    @override
    @abstractmethod
    def build(
        self,
        case: ConfT,
        conf: CaseT,
    ) -> TaskT:
        """Build exercise task."""
