"""General domain contracts."""

from typing import Generic, Protocol, TypedDict, TypeVar

ActionT = TypeVar('ActionT')
DomainStatusT = TypeVar('DomainStatusT')
DumpData_co = TypeVar('DumpData_co', covariant=True)
ContextT = TypeVar('ContextT')


class HasResourceIdentifier(Protocol):
    """Protocol for has resource identifier interface."""

    pk: int


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str


class HasValue(Protocol):
    """Protocol for has *value* interface."""

    value: int


# =================================================
# Domain action / status contracts
# =================================================


class TypedAction(TypedDict, Generic[ActionT]):
    """Typed dict for domain action."""

    action: ActionT


class TypedOptionValue(TypedDict):
    """Typed dict for option value."""

    option_value: str


class HasAction(Protocol[ActionT]):
    """Protocol for has *action* interface."""

    action: ActionT


class HasDomainStatus(Protocol[DomainStatusT]):
    """Protocol for has *domain_status* interface."""

    domain_status: DomainStatusT


# =================================================
# Item meta data
# =================================================


class HasCategory(Protocol):
    """Protocol for has *category* interface."""

    category: int | None


class HasMark(Protocol):
    """Protocol for has *mark* interface."""

    mark: list[int]


class HasSource(Protocol):
    """Protocol for has *source* interface."""

    source: int | None


# =================================================
# DTO contract
# =================================================


class DumpModelProtocol(Protocol[DumpData_co]):
    """Protocol for *model_dump* interface."""

    def model_dump(self) -> DumpData_co:
        """Dumb DTO model to dict."""
