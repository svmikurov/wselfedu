"""Core request assembler."""

from typing import Generic, TypeVar, override

from interfaces.protocols.request.general import RequestContextProtocol
from kernel.parser.request import RequestParamsQueryParserProtocol
from ports.abstract.assembler import AbstractAssembler
from ports.contract.entity.general import NullProtocol
from ports.interfaces.protocols.command import (
    QueryCommandProtocol,
    UserCommandProtocol,
    UserDataCommandProtocol,
    UserDetailCommandProtocol,
    UserDetailDataCommandProtocol,
)
from ports.interfaces.protocols.web import (
    DetailRequestParamsProtocol,
    QueryRequestParamsProtocol,
)
from ports.interfaces.schemas.command import (
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

QueryTypeT = TypeVar('QueryTypeT')
QueryDataT = TypeVar('QueryDataT')
QueryParserT = TypeVar('QueryParserT')
CommandDataT = TypeVar('CommandDataT')
ValidatedT = TypeVar('ValidatedT')

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
        ValidatedT,
        UserDataCommandProtocol[ValidatedT],
    ],
):
    """User's data request assembler."""

    @override
    def prepare(
        self,
        params: NullProtocol,
        context: RequestContextProtocol,
        data: ValidatedT,
    ) -> UserDataCommandProtocol[ValidatedT]:
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
        QueryRequestParamsProtocol[QueryDataT],
        RequestContextProtocol,
        NullProtocol,
        UserQueryCommand[QueryTypeT],
    ]
):
    """User's request parameters assembler with query."""

    def __init__(
        self,
        parser: RequestParamsQueryParserProtocol[QueryDataT, QueryTypeT],
    ) -> None:
        """Create the assembler."""
        self._parser = parser

    @override
    def prepare(
        self,
        params: QueryRequestParamsProtocol[QueryDataT],
        context: RequestContextProtocol,
        data: NullProtocol,
    ) -> UserQueryCommand[QueryTypeT]:
        """Prepare request data for use case execute."""
        return UserQueryCommand(
            query=self._parser.parse(params.query),
            user=context.user,
        )


class UserQueryDataAssembler(
    AbstractAssembler[
        QueryRequestParamsProtocol[QueryDataT],
        RequestContextProtocol,
        ValidatedT,
        UserQueryDataCommand[QueryTypeT, ValidatedT],
    ]
):
    """User's request parameters assembler with query and data."""

    def __init__(
        self,
        parser: RequestParamsQueryParserProtocol[QueryDataT, QueryTypeT],
    ) -> None:
        """Create the assembler."""
        self._parser = parser

    @override
    def prepare(
        self,
        params: QueryRequestParamsProtocol[QueryDataT],
        context: RequestContextProtocol,
        data: ValidatedT,
    ) -> UserQueryDataCommand[QueryTypeT, ValidatedT]:
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
        ValidatedT,
        UserDetailDataCommandProtocol[ValidatedT],
    ],
    Generic[ValidatedT],
):
    """User's resource data assembler."""

    @override
    def prepare(
        self,
        params: DetailRequestParamsProtocol,
        context: RequestContextProtocol,
        data: ValidatedT,
    ) -> UserDetailDataCommandProtocol[ValidatedT]:
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
        QueryRequestParamsProtocol[QueryTypeT],
        NullProtocol,
        NullProtocol,
        QueryCommandProtocol[QueryTypeT],
    ]
):
    """Detail query user context assembler."""

    @override
    def prepare(
        self,
        params: QueryRequestParamsProtocol[QueryTypeT],
        context: NullProtocol,
        data: NullProtocol,
    ) -> QueryCommandProtocol[QueryTypeT]:
        """Prepare request data for use case execute."""
        return QueryCommand(
            query=params.query,
        )
