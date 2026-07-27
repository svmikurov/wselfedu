"""Domain events."""

from dataclasses import dataclass

from .protocols import TaskProtocol


class Event:
    """Base domain event."""


###################################################
# Task events
###################################################


class TaskEvent(Event):
    """Base task event."""


class TaskRequested(TaskEvent):
    """Task was requested."""


@dataclass
class TaskCreated(TaskEvent):
    """Task was created."""

    task: TaskProtocol


class CheckRequested(TaskEvent):
    """Answer check was requested."""


class AnswerVerified(TaskEvent):
    """User's answer was correct."""


class IncorrectAnswerGiven(TaskEvent):
    """User's answer was incorrect."""
