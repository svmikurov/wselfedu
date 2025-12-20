"""Language discipline app types."""

import logging
import uuid
from typing import (
    Literal,
    NamedTuple,
    Protocol,
    TypeAlias,
    TypedDict,
)

log = logging.getLogger(__name__)

Language: TypeAlias = Literal['native', 'english']
TranslateOrder: TypeAlias = Literal['from_native', 'to_native', 'random']


# ------------
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


# -------
# Options
# -------


class Options(TypedDict):
    """Translation options type."""

    categories: list[IdName]
    marks: list[IdName]
    sources: list[IdName]
    periods: list[IdName]
    translation_orders: list[CodeName]


# --------
# Progress
# --------


class ProgressEdge(TypedDict):
    """Study progress phase edge type."""

    study: int
    repeat: int
    examine: int
    know: int


class ProgressPhase(TypedDict):
    """Study progress phase include type."""

    is_study: bool
    is_repeat: bool
    is_examine: bool
    is_know: bool


# -------------
# Study setting
# -------------


class TranslationParameters(TypedDict):
    """Translation parameters type."""

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

    question_timeout: int | None
    answer_timeout: int | None


# ----------
# Study case
# ----------


class CaseParameters(
    TranslationParameters,
    ProgressPhase,
    TranslationSettings,
):
    """Study case parameters type."""


class CaseSettings(
    Options,
    TranslationParameters,
    ProgressPhase,
    TranslationSettings,
    PresentationSettings,
):
    """Study case settings type."""


class SettingsToContext(TypedDict):
    """Type for settings to include into context for rendering."""

    # Study urls
    url: str
    progress_url: str

    # Translation parameters
    category: str
    mark: str
    word_source: str
    start_period: str
    end_period: str

    # Translation settings
    translation_order: TranslateOrder
    word_count: str

    # Presentation settings
    question_timeout: str
    answer_timeout: str


# Word study Presentation case
# ----------------------------


class CaseUUID(TypedDict):
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
    CaseUUID,
    PresentationDataT,
):
    """Word study Presentation case typed dict."""


# Word study Presentation progress
# --------------------------------


class ProgressCase(CaseUUID):
    """Word study progress case type."""

    is_known: bool


# TODO: Remove below?


class WordStudyCase(NamedTuple):
    """Word study case."""

    translation_id: int


class WordStudyParameters(NamedTuple):
    """Word study params."""

    translation_ids: list[int]
