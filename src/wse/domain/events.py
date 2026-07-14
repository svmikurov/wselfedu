"""Domain events."""


class Event:
    """Base domain event."""


class TaskCreated(Event):
    """Task was created."""


class AnswerVerified(Event):
    """User's answer was correct."""


class IncorrectAnswerGiven(Event):
    """User's answer was incorrect."""
