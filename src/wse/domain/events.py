"""Domain events."""


class Event:
    """Base domain event."""


class TaskRequested(Event):
    """Task was requested."""


class TaskCreated(Event):
    """Task was created."""


class CheckRequested(Event):
    """Answer check was requested."""


class AnswerVerified(Event):
    """User's answer was correct."""


class IncorrectAnswerGiven(Event):
    """User's answer was incorrect."""
