"""Mathematical discipline assembler types."""

from typing import TypeAlias, TypeVar

from interfaces.protocols.request.general import RequestContextProtocol
from ports.abstract.assembler import AbstractAssembler
from ports.contract.entity.general import NullProtocol
from ports.interfaces.protocols.command.assembler import (
    QueryCommandProtocol,
    UserCommandProtocol,
    UserDetailCommandProtocol,
)
from ports.interfaces.protocols.web import (
    DetailRequestParamsProtocol,
    QueryRequestParamsProtocol,
    RequestDataProtocol,
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
