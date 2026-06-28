"""Protocols for Django site interface."""

from typing import Any, Protocol, TypeVar

T_cov = TypeVar('T_cov', covariant=True)

Context_cov = TypeVar('Context_cov', covariant=True)
Data_cov = TypeVar('Data_cov', covariant=True)


###################################################
# Components
###################################################


# NOTE: Subject to future null object method additions
class NullProto(Protocol):
    """Protocol for null object."""


class HasHtml(Protocol):
    @property
    def html(self) -> str: ...


class HasContext(Protocol[T_cov]):
    @property
    def context(self) -> T_cov: ...


class HasSessionIdentifier(Protocol):
    @property
    def session_id(self) -> str: ...


class HasData(Protocol[T_cov]):
    @property
    def data(self) -> T_cov: ...


class HasQuery(Protocol[T_cov]):
    @property
    def query(self) -> T_cov: ...


class HtmlResponsible(
    HasHtml,
    HasContext[dict[str, Any]],
    Protocol,
): ...


###################################################
# Compositions
###################################################


class SimpleRequestParamsProto(
    HasQuery[NullProto],
    HasContext[Context_cov],
    HasData[Data_cov],
): ...
