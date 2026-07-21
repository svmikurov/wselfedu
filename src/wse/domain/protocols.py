"""Domain layer protocols."""

from typing import Any, Protocol, TypeVar

from .events import Event

T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

CreateTaskCommandT = TypeVar('CreateTaskCommandT', contravariant=True)
CheckAnswerCommandT = TypeVar('CheckAnswerCommandT', contravariant=True)


###################################################
# Attributes
###################################################


class HasSessionIdentifier(Protocol):
    @property
    def session_id(self) -> str: ...


class HasQuestionText(Protocol):
    @property
    def question_text(self) -> str: ...


class HasTask(Protocol[T_co]):
    @property
    def task(self) -> T_co: ...


class HasIsCorrectAnswer(Protocol):
    @property
    def is_correct_answer(self) -> bool: ...


class HasEvents(Protocol):
    @property
    def events(self) -> list[Event]: ...


class HasEventsBoolean(Protocol):
    def has_events(self) -> bool: ...


class EventPoppable(Protocol[T_co]):
    def pop_event(self) -> T_co: ...


class Handable(Protocol[T_contra, T_co]):
    def handle(self, cmd: T_contra) -> T_co: ...


###################################################
# Methods
###################################################


class Executable(Protocol[T_co]):
    def execute(self, cmd: Any) -> T_co: ...


class TaskCreatable(Protocol):
    def create_task(self) -> None: ...


class AnswerCheckable(Protocol[T_contra]):
    def check_answer(self, cmd: T_contra) -> None: ...


###################################################
# Model
###################################################


class TaskProtocol(
    HasQuestionText,
    Protocol,
): ...


class ExerciseProtocol(
    TaskCreatable,
    AnswerCheckable[CheckAnswerCommandT],
    HasTask[TaskProtocol],
    HasIsCorrectAnswer,
    HasEvents,
    Protocol[CheckAnswerCommandT],
): ...


###################################################
# Aggregate
###################################################


class EventSourcedAggregate(
    HasEventsBoolean,
    EventPoppable[Event],
    Handable[T_contra, T_co],
    Protocol[T_contra, T_co],
):
    """Aggregate that handles commands and exposes domain events."""
