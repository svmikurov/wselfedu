"""Domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from . import commands
from . import events as ev

if TYPE_CHECKING:
    from wse.domain.protocols import Executable, TaskProtocol

from wse.domain.protocols import CommandProtocol

CommandT = TypeVar('CommandT', bound=CommandProtocol)

__all__ = (
    'Exercise',
    'Task',
    'Presentation',
    'PresentationTask',
)

# REFACTOR: Add parent class for Exercise and Presentation
# with common methods


class Specification:
    """Specification."""


class Exercise(Generic[CommandT]):
    """Exercise aggregate."""

    def __init__(
        self,
        session_id: str,
        create_strategy: Executable[Specification, TaskProtocol],
        check_strategy: Executable[Specification, bool],
    ) -> None:
        self._create_strategy = create_strategy
        self._check_strategy = check_strategy

        self._session_id = session_id

        self._events: list[ev.TaskEvent] = []
        self._task: TaskProtocol | None = None
        self._is_correct_answer: bool | None = None

    def handle(self, cmd: CommandT) -> None:
        """Handle command."""
        match type(cmd):
            case commands.CreateTask:
                self.create_task()
            case commands.CheckAnswer:
                self.check_answer(cmd)
            case _:
                raise RuntimeError(
                    f'Got unexpected command: {type(cmd).__name__}'
                )

    def create_task(self) -> TaskProtocol:
        """Create a task."""
        spec = self._prepare_create_spec()
        self._task = self._create_strategy.execute(spec)
        self._emit_task_created()
        return self.task

    @property
    def task(self) -> TaskProtocol:
        """Task."""
        if self._task is None:
            raise RuntimeError('No task has been created yet')
        return self._task

    def check_answer(self, cmd: CommandT) -> bool:
        """Check a user answer."""
        if self._is_correct_answer is not None:
            raise RuntimeError('Answer already checked')

        spec = self._prepare_check_spec(cmd)
        self._is_correct_answer = self._check_strategy.execute(spec)
        self._emit_answer_checked()

        if self._is_correct_answer is True:
            self.create_task()

        return self._is_correct_answer

    @property
    def is_correct_answer(self) -> bool:
        """Whether the user's answer is correct."""
        if self._is_correct_answer is None:
            raise RuntimeError('No answer has been checked yet')
        return self._is_correct_answer

    # Specification

    def _prepare_create_spec(self) -> Specification:
        """Prepare a create task specification."""
        return Specification()

    def _prepare_check_spec(self, cmd: CommandProtocol) -> Specification:
        """Prepare a check answer specification."""
        return Specification()

    # Event

    @property
    def events(self) -> list[ev.TaskEvent]:
        """Events emitted by the exercise."""
        return self._events.copy()

    def has_events(self) -> bool:
        """Has exercise events."""
        return bool(self._events)

    def pop_event(self) -> ev.TaskEvent:
        """Pop first event."""
        event = self._events.pop()
        return event

    def _emit_task_created(self) -> None:
        if self._task is None:
            raise RuntimeError('No task has been created yet')

        task = ev.TaskCreated(task=self._task)
        self._events.append(task)

    def _emit_answer_checked(self) -> None:
        event = (
            ev.AnswerVerified()
            if self._is_correct_answer
            else ev.IncorrectAnswerGiven()
        )
        self._events.append(event)


@dataclass(frozen=True, slots=True)
class Task:
    """Task model."""

    question_text: str


@dataclass(frozen=True, slots=True)
class PresentationTask:
    """Presentation exercise task model."""

    question_text: str
    answer_text: str


class Presentation:
    """Presentation exercise."""

    def __init__(
        self,
        session_id: str,
        create_strategy: Executable[Specification, TaskProtocol],
    ) -> None:
        self._create_strategy = create_strategy

        self._session_id = session_id

        self._events: list[ev.TaskEvent] = []
        self._task: TaskProtocol | None = None

    def create(self) -> TaskProtocol:
        """Create presentation task."""
        spec = self._prepare_create_spec()
        self._task = self._create_strategy.execute(spec)
        self._emit_task_created()
        return self.task

    def _prepare_create_spec(self) -> Specification:
        """Prepare a create task specification."""
        return Specification()

    def _emit_task_created(self) -> None:
        if self._task is None:
            raise RuntimeError('No task has been created yet')

        task = ev.TaskCreated(task=self._task)
        self._events.append(task)

    @property
    def task(self) -> TaskProtocol:
        """Task."""
        if self._task is None:
            raise RuntimeError('No task has been created yet')
        return self._task
