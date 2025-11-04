"""Language discipline app types."""

import uuid
from typing import Literal, NamedTuple, TypedDict

LanguageType = Literal['native', 'english']
ProgressType = Literal['known', 'unknown']


class IdNameType(TypedDict):
    """Dict representation of entity only with its 'name' and 'ID'."""

    id: int
    name: str


class WordCaseParamsType(TypedDict):
    """Default params values typed fields."""

    category: IdNameType | None
    label: IdNameType | None
    word_count: int | None


class WordParamsType(TypedDict):
    """Fields type for Word study request."""

    categories: list[IdNameType]
    labels: list[IdNameType]
    default: WordCaseParamsType | None


class WordType(TypedDict):
    """Fields type for Word study response."""

    definition: str
    explanation: str


class WordProgressType(TypedDict):
    """Word study progress typed dict."""

    case_uuid: uuid.UUID
    progress_case: ProgressType


class WordStudyCase(NamedTuple):
    """Word study case."""

    definition_id: int


class WordStudyParams(NamedTuple):
    """Word study params."""

    ids: list[int]
