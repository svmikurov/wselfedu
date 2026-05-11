"""General interface."""

from typing import Protocol, TypeVar

from apps.users.models import Person

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
StatusT = TypeVar('StatusT')


class NullProtocol(Protocol):
    """Null interface."""


class HasResourceIdentifier(Protocol):
    """Protocol for has resource identifier interface."""

    pk: int


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str


class HasException(Protocol[T]):
    """Protocol for has *exception* interface."""

    exception: T


class HasStatus(Protocol[T_co]):
    """Protocol for has *status* interface."""

    @property
    def status(self) -> T_co:
        """Status."""


class HasContext(Protocol[T]):
    """Protocol for has *context* interface."""

    context: T


class HasExtraContext(Protocol[T]):
    """Protocol for has *extra_context* interface."""

    extra_context: T


class HasIsHtmx(Protocol):
    """Protocol for has *is_htmx* interface."""

    is_htmx: bool


class PersonProtocol(Protocol):
    """Protocol for user interface."""

    pk: int
    username: str


class HasUser(Protocol):
    """Protocol for has *user* interface."""

    user: Person


class HasData(Protocol[T_co]):
    """Protocol for has *data* interface."""

    @property
    def data(self) -> T_co:
        """Provide data."""
