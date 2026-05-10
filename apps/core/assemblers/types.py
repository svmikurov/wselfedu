"""Mathematical discipline assembler types."""

from typing import TypeAlias, TypeVar

from apps.core.handlers.protocol import (
    DetailRequestParamsProtocol,
    QueryRequestParamsProtocol,
    RequestDataProtocol,
)
from contracts.entity.general import NullProtocol
from interfaces.protocols.request.general import RequestContextProtocol
from ports.contract.entity.command import (
    QueryCommandProtocol,
    UserCommandProtocol,
    UserDetailCommandProtocol,
)

from .abstract import AbstractAssembler

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
