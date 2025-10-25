"""Language discipline app types."""

from typing import NamedTuple, TypedDict


class WordParamsType(TypedDict):
    """Fields type for Word study request."""

    category: list[str] | None
    marks: list[str] | None
    user_id: int


class WordType(TypedDict):
    """Fields type for Word study response."""

    definition: str
    explanation: str


class WordStudyCase(NamedTuple):
    """Word study case."""

    definition_id: int


class WordStudyParams(NamedTuple):
    """Word study params."""

    ids: list[int]
