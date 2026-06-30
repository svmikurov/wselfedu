"""HTTP response context interface."""

from typing import TypedDict


class CreateTestingTaskContext(TypedDict):
    """Typed context for create testing task response."""

    question_text: str
