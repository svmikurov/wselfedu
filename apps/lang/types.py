"""Language discipline app types."""

from typing import NamedTuple, TypedDict


class IdNameType(TypedDict):
    """Dict representation of entity only with its 'name' and 'ID'."""

    id: int
    name: str


class WordParamsType(TypedDict):
    """Fields type for Word study request."""

    user_id: int
    categories: list[IdNameType]
    labels: list[IdNameType]


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
