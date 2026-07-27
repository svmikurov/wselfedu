"""Application layer commands."""

from dataclasses import dataclass


class Command:
    """Base command."""


@dataclass(frozen=True, slots=True)
class TaskCommand(Command):
    """Base task command."""

    session_id: str


@dataclass(frozen=True, slots=True)
class CreateTask(TaskCommand):
    """Create task command."""


@dataclass(frozen=True, slots=True)
class CheckAnswer(TaskCommand):
    """Check user answer command."""
