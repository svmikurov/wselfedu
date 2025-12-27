"""Protocols for the interface of refactored and new objects."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Literal,
    Protocol,
    TypedDict,
    TypeVar,
)

if TYPE_CHECKING:
    from apps.users.models import Person

type TranslationOrder = Literal['to_native', 'to_foreign', 'random']

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)

# --------------------
# UseCase dependencies
# --------------------


class Validator(Protocol[T_contra, T_co]):
    """Protocol for validator interface."""

    @classmethod
    def validate(cls, raw_data: T_contra) -> T_co:
        """Validate raw data."""


class BusinessService(Protocol[T_contra, T_co]):
    """Protocol for business service interface."""

    def execute(self, user: Person, query_parameters: T_contra) -> T_co:
        """Execute business logic."""


class ResponseAdapter(Protocol[T_contra, T_co]):
    """Protocol for response adapter interface."""

    def to_response(self, domain_result: T_contra) -> T_co:
        """Convert to response."""


# --------------
# Web data types
# --------------


class WebRequestRaw(TypedDict):
    """Get presentation web request raw data types."""

    category: str
    mark: list[str]
    source: str
    start_period: str
    end_period: str

    is_study: str
    is_repeat: str
    is_examine: str
    is_know: str

    translation_order: TranslationOrder
    word_count: str


class WebRequest(TypedDict):
    """Get presentation web request validated data types.

    No optional typed fields provides with default value.
    """

    category: int | None
    mark: list[int]
    source: int | None
    start_period: int | None
    end_period: int | None

    is_study: bool
    is_repeat: bool
    is_examine: bool
    is_know: bool

    translation_order: TranslationOrder
    word_count: int | None


# --------------
# Api data types
# --------------


class IdName(TypedDict):
    """Id-name option type."""

    id: int
    name: str


class CodeName(TypedDict):
    """Code-name option type."""

    code: TranslationOrder
    name: str


class ApiRequest(TypedDict):
    """Get presentation api request data types.

    No optional typed fields provides with default value.
    """

    category: IdName | None
    mark: list[IdName]
    word_source: IdName | None
    start_period: IdName | None
    end_period: IdName | None

    is_study: bool
    is_repeat: bool
    is_examine: bool
    is_know: bool

    translation_order: CodeName
    word_count: int | None
