"""Domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from . import events

if TYPE_CHECKING:
    from wse.domain.protocols import Executable, TaskProtocol

CheckAnswerCommandT = TypeVar('CheckAnswerCommandT')

__all__ = (
    'Exercise',
    'Task',
)


class Specification:
    """Specification."""


class Exercise(Generic[CheckAnswerCommandT]):
    """Exercise aggregate."""

    def __init__(
        self,
        session_id: str,
        create_strategy: Executable[TaskProtocol],
        check_strategy: Executable[bool],
    ) -> None:
        self._create_strategy = create_strategy
        self._check_strategy = check_strategy

        self._session_id = session_id

        self._events: list[events.Event] = list()
        self._task: TaskProtocol | None = None
        self._is_correct_answer: bool | None = None

    def handle(self, event: events.Event) -> None:
        """Handle event."""
        match type(event):
            case events.TaskRequested:
                self.create_task()
            case events.CheckRequested:
                self.check_answer(event)

    def create_task(self) -> None:
        """Create a task."""
        spec = self._prepare_create_spec()
        self._task = self._create_strategy.execute(spec)
        self._emit_task_created()

    def check_answer(self, event: events.Event) -> None:
        """Check a user answer."""
        if self._is_correct_answer is not None:
            raise RuntimeError('Answer already checked')

        spec = self._prepare_check_spec()
        self._is_correct_answer = self._check_strategy.execute(spec)
        self._emit_answer_checked()

        if self._is_correct_answer is True:
            self.create_task()

    # Specification

    def _prepare_create_spec(self) -> Specification:
        """Prepare a create task specification."""
        return Specification()

    def _prepare_check_spec(self) -> Specification:
        """Prepare a check answer specification."""
        return Specification()

    # Event methods

    def _emit_task_created(self) -> None:
        self._events.append(events.TaskCreated())

    def _emit_answer_checked(self) -> None:
        event = (
            events.AnswerVerified()
            if self._is_correct_answer
            else events.IncorrectAnswerGiven()
        )
        self._events.append(event)

    # Properties

    @property
    def task(self) -> TaskProtocol:
        """Task."""
        if self._task is None:
            raise RuntimeError('No task has been created yet')
        return self._task

    @property
    def is_correct_answer(self) -> bool:
        """Whether the user's answer is correct."""
        if self._is_correct_answer is None:
            raise RuntimeError('No answer has been checked yet')
        return self._is_correct_answer

    @property
    def events(self) -> list[events.Event]:
        """Events emitted by the exercise."""
        return self._events.copy()


@dataclass(frozen=True, slots=True)
class Task:
    """Task model."""

    question_text: str
