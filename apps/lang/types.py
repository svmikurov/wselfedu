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
    default_params: WordCaseParamsType | None


class CaseUUIDType(TypedDict):
    """Case UUID typed dict."""

    case_uuid: uuid.UUID


class PresentationDict(TypedDict):
    """Word study Presentation typed dict."""

    definition: str
    explanation: str


class WordCaseType(
    CaseUUIDType,
    PresentationDict,
):
    """Word study case typed dict."""


class WordProgressType(CaseUUIDType):
    """Word study progress typed dict."""

    progress_type: ProgressType


class WordStudyCase(NamedTuple):
    """Word study case."""

    translation_id: int


class WordStudyParams(NamedTuple):
    """Word study params."""

    translation_ids: list[int]
