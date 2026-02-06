"""Fixture types."""

from typing import TypedDict


class PresentationCaseDict(TypedDict):
    """TypedDict for presentation exercise case fixture data.

    Used by Pydantic models to validate fixture structure and types.
    """

    question_text: str
    answer_text: str
    progress: int
