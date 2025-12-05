"""Language discipline app types."""

import logging
import uuid
from datetime import datetime
from typing import (
    Literal,
    NamedTuple,
    Protocol,
    TypeAlias,
    TypedDict,
)

log = logging.getLogger(__name__)

Language: TypeAlias = Literal['native', 'english']
Progress: TypeAlias = Literal['known', 'unknown']
TranslateOrder: TypeAlias = Literal['from_native', 'to_native', 'random']


# Option types
# ------------


class HasIdName(Protocol):
    """Protocol for id-name option interface."""

    id: int
    name: str


class IdName(TypedDict):
    """Id-name option type."""

    id: int
    name: str


class CodeName(TypedDict):
    """Code-name option type."""

    code: str
    name: str


# Word
# ----


class Options(TypedDict):
    """Translation options type."""

    categories: list[IdName]
    marks: list[IdName]
    sources: list[IdName]
    periods: list[IdName]
    translation_orders: list[CodeName]


class TranslationMeta(TypedDict):
    """Translation meta type."""

    category: IdName | None
    mark: IdName | None
    word_source: IdName | None
    start_period: IdName | None
    end_period: IdName | None


class TranslationSettings(TypedDict):
    """Translation settings type."""

    translation_order: CodeName | None
    word_count: int | None


class PresentationSettings(TypedDict):
    """Presentation settings type."""

    question_timeout: float | None
    answer_timeout: float | None


# Word study
# ----------


class WordLookup(TypedDict, total=False):
    """Word lookup condition type."""

    category: int | None
    marks: int | None
    source: int | None
    start_period: datetime | None
    end_period: datetime | None


class WordParameters(
    TranslationMeta,
    TranslationSettings,
):
    """Word parameters type."""


class StudyParameters(
    WordParameters,
    PresentationSettings,
):
    """Word study parameters types."""


class SetStudyParameters(
    Options,
    StudyParameters,
):
    """Set Word study parameters types."""


# Word study Presentation case
# ----------------------------


class CaseUUIDType(TypedDict):
    """Case UUID typed dict."""

    case_uuid: uuid.UUID


class PresentationT(TypedDict):
    """Word study Presentation typed dict."""

    definition: str
    explanation: str


class InfoT(TypedDict):
    """Word study Presentation info typed dict."""

    progress: int | None


class PresentationDataT(
    PresentationT,
):
    """Word study Presentation data typed dict."""

    info: InfoT


class PresentationCaseT(
    CaseUUIDType,
    PresentationDataT,
):
    """Word study Presentation case typed dict."""


# Word study Presentation progress
# --------------------------------


class WordProgressT(CaseUUIDType):
    """Word study progress typed dict."""

    progress_type: Progress


# TODO: Remove below?


class WordStudyCase(NamedTuple):
    """Word study case."""

    translation_id: int


class WordStudyParameters(NamedTuple):
    """Word study params."""

    translation_ids: list[int]
