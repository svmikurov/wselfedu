"""Abstract base classes for domain service."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, override

from wse.domain.protocols import (
    AnswerCheckableService,
    CreateTaskServiceProtocol,
    UniqueLearnable,
)

ResultT = TypeVar('ResultT')
AnswerT = TypeVar('AnswerT')


class AbstractCreateTaskService(
    ABC,
    CreateTaskServiceProtocol[ResultT],
):
    """ABC for create task service."""

    @override
    @abstractmethod
    def execute(self, candidates: list[UniqueLearnable]) -> ResultT:
        """Create the task."""


class AbstractCheckAnswerService(
    ABC,
    AnswerCheckableService[AnswerT, ResultT],
):
    """ABC for check answer service."""

    @override
    @abstractmethod
    def execute(self, spec: AnswerT) -> ResultT:
        """Check the answer."""
