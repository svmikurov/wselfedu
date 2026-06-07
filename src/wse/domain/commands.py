"""Commands."""

from dataclasses import dataclass

from . import enums


class Command:
    """Base command."""


@dataclass(frozen=True, slots=True)
class CreateTaskCommand(Command):
    """Create a new task command."""

    action: enums.ExerciseAction = enums.ExerciseAction.CREATE_TASK


@dataclass(frozen=True, slots=True)
class CheckAnswerCommand(Command):
    """Check a user answer command."""

    action: enums.ExerciseAction = enums.ExerciseAction.CHECK_ANSWER
