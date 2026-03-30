"""Core request assembler."""

from typing import Generic, TypeVar, override

from apps.core.assemblers.protocol import (
    QueryCommandProtocol,
    UserCommandProtocol,
    UserDataCommandProtocol,
    UserDetailCommandProtocol,
    UserDetailDataCommandProtocol,
)
from apps.core.handlers.protocol import (
    DetailRequestParamsProtocol,
    NullProtocol,
    QueryRequestParamsProtocol,
    RequestContextProtocol,
)
from apps.core.parsers.protocol import RequestParamsQueryParserProtocol

from .abstract import AbstractAssembler
from .command import (
    QueryCommand,
    UserCommand,
    UserDataCommand,
    UserDetailCommand,
    UserDetailDataCommand,
    UserQueryCommand,
    UserQueryDataCommand,
)
from .types import (
    UserAssemblerType,
    UserDetailAssemblerType,
)

__all__ = (
    'UserQueryAssembler',
    'UserAssembler',
    'UserDetailAssembler',
    'UserDetailDataAssembler',
)

QueryType = TypeVar('QueryType')
QueryData = TypeVar('QueryData')
QueryParser = TypeVar('QueryParser')
CommandData = TypeVar('CommandData')
Validated = TypeVar('Validated')

# =================================================
# Login required
# =================================================


class UserAssembler(UserAssemblerType):
    """User's request assembler."""

    @override
    def prepare(
        self,
        params: NullProtocol,
        context: RequestContextProtocol,
        data: NullProtocol,
    ) -> UserCommandProtocol:
        """Prepare request data for use case execute."""
        return UserCommand(
            user=context.user,
        )


class UserDataAssembler(
    AbstractAssembler[
        NullProtocol,
        RequestContextProtocol,
        Validated,
        UserDataCommandProtocol[Validated],
    ],
):
    """User's data request assembler."""

    @override
    def prepare(
        self,
        params: NullProtocol,
        context: RequestContextProtocol,
        data: Validated,
    ) -> UserDataCommandProtocol[Validated]:
        """Prepare request data for use case execute."""
        return UserDataCommand(
            user=context.user,
            data=data,
        )


# -------------------------------------------------
# Query
# -------------------------------------------------


class UserQueryAssembler(
    AbstractAssembler[
        QueryRequestParamsProtocol[QueryData],
        RequestContextProtocol,
        NullProtocol,
        UserQueryCommand[QueryType],
    ]
):
    """User's request parameters assembler with query."""

    def __init__(
        self,
        parser: RequestParamsQueryParserProtocol[QueryData, QueryType],
    ) -> None:
        """Create the assembler."""
        self._parser = parser

    @override
    def prepare(
        self,
        params: QueryRequestParamsProtocol[QueryData],
        context: RequestContextProtocol,
        data: NullProtocol,
    ) -> UserQueryCommand[QueryType]:
        """Prepare request data for use case execute."""
        return UserQueryCommand(
            query=self._parser.parse(params.query),
            user=context.user,
        )


class UserQueryDataAssembler(
    AbstractAssembler[
        QueryRequestParamsProtocol[QueryData],
        RequestContextProtocol,
        Validated,
        UserQueryDataCommand[QueryType, Validated],
    ]
):
    """User's request parameters assembler with query and data."""

    def __init__(
        self,
        parser: RequestParamsQueryParserProtocol[QueryData, QueryType],
    ) -> None:
        """Create the assembler."""
        self._parser = parser

    @override
    def prepare(
        self,
        params: QueryRequestParamsProtocol[QueryData],
        context: RequestContextProtocol,
        data: Validated,
    ) -> UserQueryDataCommand[QueryType, Validated]:
        """Prepare request data for use case execute."""
        return UserQueryDataCommand(
            query=self._parser.parse(params.query),
            user=context.user,
            data=data,
        )


# -------------------------------------------------
# Detail
# -------------------------------------------------


class UserDetailAssembler(UserDetailAssemblerType):
    """User's resource request assembler."""

    @override
    def prepare(
        self,
        params: DetailRequestParamsProtocol,
        context: RequestContextProtocol,
        data: NullProtocol,
    ) -> UserDetailCommandProtocol:
        """Prepare request data for use case execute."""
        return UserDetailCommand(
            user=context.user,
            pk=params.pk,
        )


class UserDetailDataAssembler(
    AbstractAssembler[
        DetailRequestParamsProtocol,
        RequestContextProtocol,
        Validated,
        UserDetailDataCommandProtocol[Validated],
    ],
    Generic[Validated],
):
    """User's resource data assembler."""

    @override
    def prepare(
        self,
        params: DetailRequestParamsProtocol,
        context: RequestContextProtocol,
        data: Validated,
    ) -> UserDetailDataCommandProtocol[Validated]:
        """Prepare request data for use case execute."""
        return UserDetailDataCommand(
            user=context.user,
            pk=params.pk,
            data=data,
        )


# =================================================
# Login not required
# =================================================


class DetailQueryContextAssembler(
    AbstractAssembler[
        QueryRequestParamsProtocol[QueryType],
        NullProtocol,
        NullProtocol,
        QueryCommandProtocol[QueryType],
    ]
):
    """Detail query user context assembler."""

    @override
    def prepare(
        self,
        params: QueryRequestParamsProtocol[QueryType],
        context: NullProtocol,
        data: NullProtocol,
    ) -> QueryCommandProtocol[QueryType]:
        """Prepare request data for use case execute."""
        return QueryCommand(
            query=params.query,
        )
