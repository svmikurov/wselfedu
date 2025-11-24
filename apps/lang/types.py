"""Language discipline app types."""

import uuid
from typing import Literal, NamedTuple, Protocol, TypedDict

LanguageType = Literal['native', 'english']
ProgressType = Literal['known', 'unknown']
TranslateOrderT = Literal['from_native', 'to_native', 'random']


class HasIdName(Protocol):
    """Protocol for id-name dictionaries."""

    id: int
    name: str


class IdName(TypedDict):
    """Dict representation of entity only with its 'name' and 'ID'."""

    id: int
    name: str


class CodeName(TypedDict):
    """Dict representation of choice with machine and human values."""

    code: str
    name: str


# Word study Presentation params
# ------------------------------


# TODO: Rename to `ParamOptionsT`
class ParamsChoicesT(TypedDict):
    """Fields type for Word study choices."""

    categories: list[IdName] | None
    marks: list[IdName] | None
    sources: list[IdName] | None
    periods: list[IdName]
    translation_orders: list[CodeName]


class InitialChoicesT(TypedDict):
    """Fields type for Word study initial choices."""

    category: IdName | None
    mark: IdName | None
    word_source: IdName | None
    # TODO: Should below fields be optional?
    translation_order: CodeName | None
    start_period: IdName | None
    end_period: IdName | None


class PresentationSettingsT(TypedDict):
    """Fields type for Word study Presentation settings."""

    word_count: int | None
    question_timeout: float | None
    answer_timeout: float | None


class UpdateParametersT(InitialChoicesT, PresentationSettingsT):
    """Fields type to Word study Presentation parameters."""


class WordPresentationParamsT(
    ParamsChoicesT,
    InitialChoicesT,
    PresentationSettingsT,
):
    """Fields type for Word study response."""


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

    info: InfoT | None


class PresentationCaseT(
    CaseUUIDType,
    PresentationDataT,
):
    """Word study Presentation case typed dict."""


# Word study Presentation progress
# --------------------------------


class WordProgressT(CaseUUIDType):
    """Word study progress typed dict."""

    progress_type: ProgressType


# TODO: Remove below?


class WordStudyCase(NamedTuple):
    """Word study case."""

    translation_id: int


class WordStudyParams(NamedTuple):
    """Word study params."""

    translation_ids: list[int]
