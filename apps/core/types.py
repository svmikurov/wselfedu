"""Types for project objects."""

from typing import NotRequired, TypedDict


class RelatedDataType(TypedDict):
    """Type for exercise related data."""

    balance: str


class ResultType(TypedDict):
    """Type for answer validation result."""

    is_correct: bool
    correct_answer: NotRequired[str]
    user_answer: NotRequired[str]
