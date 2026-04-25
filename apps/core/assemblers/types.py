"""Mathematical discipline assembler types."""

from typing import TypeAlias, TypeVar

from apps.core.handlers.protocol import (
    DetailRequestParamsProtocol,
    QueryRequestParamsProtocol,
    RequestContextProtocol,
    RequestDataProtocol,
)
from interfaces.protocols.general import NullProtocol

from .abstract import AbstractAssembler
from .protocol import (
    QueryCommandProtocol,
    UserCommandProtocol,
    UserDetailCommandProtocol,
)

QueryData = TypeVar('QueryData')
QueryType = TypeVar('QueryType')
Validated = TypeVar('Validated')
CommandData = TypeVar('CommandData')


QueryAssemblerType: TypeAlias = AbstractAssembler[
    QueryRequestParamsProtocol[QueryData],
    RequestContextProtocol,
    NullProtocol,
    QueryCommandProtocol[QueryType],
]

UserAssemblerType: TypeAlias = AbstractAssembler[
    NullProtocol,
    RequestContextProtocol,
    NullProtocol,
    UserCommandProtocol,
]

UserDetailAssemblerType: TypeAlias = AbstractAssembler[
    DetailRequestParamsProtocol,
    RequestContextProtocol,
    NullProtocol,
    UserDetailCommandProtocol,
]

DetailContextDataAssemblerType: TypeAlias = AbstractAssembler[
    DetailRequestParamsProtocol,
    RequestContextProtocol,
    RequestDataProtocol[Validated],
    UserDetailCommandProtocol,
]
