"""Language discipline app types."""

import logging
import uuid
from typing import (
    Literal,
    NamedTuple,
    Protocol,
    TypedDict,
)

log = logging.getLogger(__name__)

type Language = Literal['native', 'english']
type TranslateOrder = Literal['from_native', 'to_native', 'random']
type Progress = Literal['is_study', 'is_repeat', 'is_examine', 'is_know']
type Option = Literal[
    'category', 'mark', 'word_source', 'start_period', 'end_period'
]


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

    code: TranslateOrder
    name: str


# -------
# Options
# -------


class OptionsAPI(TypedDict):
    """Translation options API type."""

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


class TranslationParametersAPI(TypedDict):
    """Translation parameters API type."""

    category: IdName | None
    mark: list[IdName]
    word_source: IdName | None
    start_period: IdName | None
    end_period: IdName | None


class TranslationSettingsAPI(TypedDict):
    """Translation settings API type."""

    translation_order: CodeName | None
    word_count: int | None


class PresentationSettings(TypedDict):
    """Presentation settings type."""

    question_timeout: int | None
    answer_timeout: int | None


# ----------
# Study case
# ----------


class CaseParametersAPI(
    TranslationParametersAPI,
    ProgressPhase,
    TranslationSettingsAPI,
):
    """Study case parameters type."""


class CaseSettingsAPI(
    OptionsAPI,
    CaseParametersAPI,
    PresentationSettings,
):
    """Study case settings API type."""


# ---------------------------
# Study settings domain types
# ---------------------------


class CaseSettingsDomain(TypedDict):
    """Case settings context type."""

    # Translation parameters
    category: int | None
    word_source: int | None | None
    mark: list[int]
    start_period: int | None
    end_period: int | None

    # Progress phases
    is_study: bool
    is_repeat: bool
    is_examine: bool
    is_know: bool

    # Translation settings
    translation_order: TranslateOrder | None
    word_count: int | None


# ------------------------
# Study settings WEB types
# ------------------------


class CaseSettingsWEB(TypedDict):
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


class CaseStudySettingsWEB(
    CaseSettingsWEB,
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

    question: str
    answer: str


class InfoT(TypedDict):
    """Word study Presentation info typed dict."""

    progress: int | None


# ----------------
# WEB presentation
# ----------------


class UpdateProgressT(TypedDict):
    """Update progress typed dict."""

    case_uuid: str
    is_known: Literal['true', 'false']


class ProgressT(TypedDict):
    """Study progress type dict."""

    current: str
    update_url: str
    increment_payload: str
    decrement_payload: str


class TranslationWEB(TypedDict):
    """Type for study case to include into context for rendering."""

    case_uuid: str
    question: str
    answer: str
    progress: ProgressT


class TranslationAPI(TypedDict):
    """Type for study case to include into context for rendering."""

    case_uuid: uuid.UUID
    question: str
    answer: str
    progress: str


# Word study Presentation case
# ----------------------------


class PresentationDataT(
    PresentationT,
):
    """Word study Presentation data typed dict."""

    info: InfoT


# TODO: Refactor, update to NamedTuple?
class TranslationCase(
    CaseUUID,
    PresentationDataT,
):
    """Word study Presentation case typed dict."""


class TranslationCaseFixed(
    PresentationDataT,
):
    """Word study Presentation case typed dict."""

    case_uuid: str


# Word study Presentation progress
# --------------------------------


class ProgressCase(CaseUUID):
    """Word study progress case type."""

    is_known: bool


# TODO: Remove below?


class WordStudyCase(NamedTuple):
    """Word study case."""

    translation_id: int


class CaseCandidates(NamedTuple):
    """Collection type of candidates to presentation case."""

    translation_ids: list[int]
