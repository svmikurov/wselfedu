"""Protocol for use case interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from utils.audit.protocol import Auditable

if TYPE_CHECKING:
    from apps.users.models import Person

Params_contra = TypeVar('Params_contra', contravariant=True)
Context_contra = TypeVar('Context_contra', contravariant=True)
Validated_contra = TypeVar('Validated_contra', contravariant=True)
CommandData_cov = TypeVar('CommandData_cov', covariant=True)

Validated = TypeVar('Validated')
QueryType = TypeVar('QueryType')

# =================================================
# Assembler's protocol
# =================================================


class AssemblerProtocol(
    Auditable,
    Protocol[
        Params_contra,
        Context_contra,
        Validated_contra,
        CommandData_cov,
    ],
):
    """Protocol for assembler interface."""

    def prepare(
        self,
        params: Params_contra,
        context: Context_contra,
        data: Validated_contra,
    ) -> CommandData_cov:
        """Prepare request data for use case execute."""


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
