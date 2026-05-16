"""Protocol for use case interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

Validated = TypeVar('Validated')
QueryType = TypeVar('QueryType')


# =================================================
# Base command's protocol
# =================================================


class QueryCommandProtocol(Protocol[QueryType]):
    """Protocol for query command."""

    query: QueryType


class UserCommandProtocol(Protocol):
    """Protocol for user's command."""

    user: Person


class DetailCommandProtocol(Protocol):
    """Protocol for detail resource command."""

    pk: int


class DataCommandProtocol(Protocol[Validated]):
    """Protocol for data command."""

    data: Validated


# =================================================
# Derived command's protocol
# =================================================


class UserQueryCommandProtocol(
    UserCommandProtocol,
    QueryCommandProtocol[QueryType],
    Protocol,
):
    """Protocol for user's query command."""


class UserDetailCommandProtocol(
    UserCommandProtocol,
    DetailCommandProtocol,
    Protocol,
):
    """Protocol for user's resource command."""


class UserDataCommandProtocol(
    UserCommandProtocol,
    DataCommandProtocol[Validated],
    Protocol,
):
    """Protocol for user's data command."""


class UserQueryDataCommandProtocol(
    UserCommandProtocol,
    QueryCommandProtocol[QueryType],
    DataCommandProtocol[Validated],
    Protocol,
):
    """Protocol for user's query data command."""


class UserDetailDataCommandProtocol(
    UserCommandProtocol,
    DetailCommandProtocol,
    DataCommandProtocol[Validated],
    Protocol,
):
    """Protocol for user's resource data command."""


class DetailQueryContextCommandProtocol(
    DetailCommandProtocol,
    QueryCommandProtocol[QueryType],
    UserCommandProtocol,
    Protocol,
):
    """Protocol for detail user query command."""


class DetailQueryContextDataCommandProtocol(
    DetailCommandProtocol,
    QueryCommandProtocol[QueryType],
    UserCommandProtocol,
    DataCommandProtocol[Validated],
    Protocol,
):
    """Protocol for detail query user data command."""
