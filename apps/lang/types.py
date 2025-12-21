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
    CaseParameters,
    PresentationSettings,
):
    """Study case settings type."""


# ----------------------------------------
# Study settings types in response context
# ----------------------------------------


class CaseSettingContext(TypedDict):
    """Case settings context type."""

    # Translation parameters
    category: str
    word_source: str
    mark: str
    start_period: str
    end_period: str

    # Progress phases
    is_study: str
    is_repeat: str
    is_examine: str
    is_know: str

    # Translation settings
    translation_order: TranslateOrder
    word_count: str


class CaseStudySettingsContext(
    CaseSettingContext,
):
    """Case study settings context type."""

    # Presentation settings
    question_timeout: str
    answer_timeout: str


# Case date


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


class CaseToContext(
    CaseUUID,
    PresentationT,
):
    """Type for study case to include into context for rendering."""

    info: InfoT


# Word study Presentation case
# ----------------------------


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
