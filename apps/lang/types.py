"""Language discipline app types."""

from typing import TypedDict


class WordParamsType(TypedDict):
    """Fields type for Word study request."""

    category: list[str] | None
    marks: list[str] | None


class WordType(TypedDict):
    """Fields type for Word study response."""

    definition: str
    explanation: str
