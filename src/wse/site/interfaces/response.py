"""HTTP response context interface."""

from typing import TypedDict


class TestingOptionContext(TypedDict):
    """Typed context for testing option."""

    value: int
    text: str


class CreateTestingTaskContext(TypedDict):
    """Typed context for create testing task response."""

    question_text: str
    options: list[TestingOptionContext]
