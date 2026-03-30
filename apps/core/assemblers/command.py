"""Assembler's command DTOs for use case's 'execute()' method."""

from typing import Generic, TypeVar

from pydantic import Field

from apps.core.domains.dto import ArbitraryDTO, BaseDTO
from apps.users.models import Person

QueryType = TypeVar('QueryType')
Validated = TypeVar('Validated')

# =================================================
# Base command
# =================================================


class QueryCommand(BaseDTO, Generic[QueryType]):
    """Query parameters command DTO."""

    query: QueryType


class UserCommand(ArbitraryDTO):
    """User's command DTO."""

    user: Person


class DetailCommand(BaseDTO):
    """Detail command DTO."""

    pk: int = Field(
        description='Resource pk',
    )


class DataCommand(BaseDTO, Generic[Validated]):
    """Detail command DTO."""

    data: Validated


# =================================================
# Derived command
# =================================================


class UserQueryCommand(
    UserCommand,
    QueryCommand[QueryType],
    Generic[QueryType],
):
    """User's query command DTO."""


class UserDataCommand(
    UserCommand,
    DataCommand[Validated],
    Generic[Validated],
):
    """User's data command DTO."""


class UserQueryDataCommand(
    UserCommand,
    QueryCommand[QueryType],
    DataCommand[Validated],
    Generic[QueryType, Validated],
):
    """User's query data command DTO."""


class UserDetailCommand(UserCommand, DetailCommand):
    """User's detail command DTO."""


class UserDetailDataCommand(
    UserCommand,
    DetailCommand,
    DataCommand[Validated],
    Generic[Validated],
):
    """User's detail data command DTO."""


class UserDetailQueryCommand(
    UserCommand,
    DetailCommand,
    QueryCommand[dict[str, str]],
):
    """User's detail data command DTO."""


class UserDetailQueryDataCommand(
    UserCommand,
    DetailCommand,
    QueryCommand[dict[str, str]],
    DataCommand[Validated],
    Generic[Validated],
):
    """User's detail query command DTO."""
