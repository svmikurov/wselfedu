"""Domain layer protocols."""

from typing import Protocol, TypeVar

Command_contra = TypeVar('Command_contra', contravariant=True)
EventT = TypeVar('EventT')
Event_co = TypeVar('Event_co', covariant=True)
Task_co = TypeVar('Task_co', covariant=True)
Result_co = TypeVar('Result_co', covariant=True)

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


class HasTask(Protocol[Task_co]):
    @property
    def task(self) -> Task_co: ...


class HasIsCorrectAnswer(Protocol):
    @property
    def is_correct_answer(self) -> bool: ...


class HasEvents(Protocol[EventT]):
    @property
    def events(self) -> list[EventT]: ...


class HasEventsBoolean(Protocol):
    def has_events(self) -> bool: ...


class EventPoppable(Protocol[Event_co]):
    def pop_event(self) -> Event_co: ...


class Handable(Protocol[Command_contra, Result_co]):
    def handle(self, cmd: Command_contra) -> Result_co: ...


###################################################
# Methods
###################################################


class Executable(Protocol[Command_contra, Result_co]):
    def execute(self, cmd: Command_contra) -> Result_co: ...


class TaskCreatable(Protocol[Task_co]):
    def create_task(self) -> Task_co: ...


class AnswerCheckable(Protocol[Command_contra]):
    def check_answer(self, cmd: Command_contra) -> bool: ...


###################################################
# Aggregate composition
###################################################


class EventSourcedAggregate(
    HasEventsBoolean,
    EventPoppable[Event_co],
    Handable[Command_contra, Result_co],
    Protocol[Command_contra, Result_co, Event_co],
):
    """Aggregate that handles commands and exposes domain events."""


class EventSourcedExercise(
    EventSourcedAggregate[Command_contra, Result_co, Event_co],
    HasTask[Task_co],
    Protocol[Command_contra, Result_co, Event_co, Task_co],
):
    """Aggregate that handles commands and exposes domain events."""


###################################################
# Commands
###################################################


class CommandProtocol(Protocol): ...


###################################################
# Model
###################################################


class TaskProtocol(
    HasQuestionText,
    Protocol,
): ...


class ExerciseProtocol(
    TaskCreatable[Task_co],
    AnswerCheckable[Command_contra],
    Handable[Command_contra, Result_co],
    HasTask[Task_co],
    HasIsCorrectAnswer,
    EventPoppable[Event_co],
    HasEventsBoolean,
    HasEvents[EventT],
    Protocol[Command_contra, Event_co, EventT, Task_co, Result_co],
): ...
