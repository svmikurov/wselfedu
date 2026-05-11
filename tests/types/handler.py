"""Handler dependencies type aliases."""

from typing import Any, TypeAlias

from interfaces.protocols.domain.exercise import (
    CandidatesT,
    ExerciseConfigProtocol,
)
from interfaces.protocols.request.general import RequestContextProtocol
from interfaces.schemas.domain.exercise import (
    PresentationExerciseDomainResult,
    TestExerciseDomainResult,
)
from kernel.handler.generic import RequestHandler
from ports.contract.entity.domain.exercise.fields import HasDomain
from ports.contract.entity.general import NullProtocol
from ports.contract.infra.adapter import AdapterProtocol
from ports.contract.infra.builder import SpecDtoBuilderProtocol
from ports.contract.infra.domain.exercise import CreateTaskDomainProtocol
from ports.contract.infra.repository import RepositoryProtocol
from ports.contract.infra.service import UserSpecServiceProtocol
from ports.contract.infra.use_case import UseCaseProtocol
from ports.contract.infra.validator import RequestValidatorProtocol
from ports.interfaces.protocols.command import AuditableAssemblerProtocol
from ports.interfaces.protocols.web import RequestDataProtocol

# HACK: Fix Any type hint
# HACK: Fix dependency from implementation

# =================================================
# Request's DTOs
# =================================================

RequestParamsT: TypeAlias = NullProtocol
"""Request parameters DTO.
"""
RequestContextT: TypeAlias = RequestContextProtocol
"""Request context DTO.
"""
RequestDataT: TypeAlias = RequestDataProtocol[Any]
"""Request body data DTO.
"""

# =================================================
# Inner DTOs
# =================================================

ValidatedT: TypeAlias = Any
"""Validated request body data DTO.
"""
CommandDataT: TypeAlias = Any
"""Combined DTO with request's parameters, context
and validated request's body data.
"""
DomainResultT: TypeAlias = Any
"""Domain result DTO.
"""
UseCaseResultT: TypeAlias = Any
"""Adapted domain result to return by use case.
"""

# =================================================
# Response's DTOs
# =================================================

ResponseDataT: TypeAlias = Any


# =================================================
# Handler dependencies
# =================================================

ValidatorT: TypeAlias = RequestValidatorProtocol[
    RequestDataT,
    ValidatedT,
]
AssemblerT: TypeAlias = AuditableAssemblerProtocol[
    RequestParamsT,
    RequestContextT,
    ValidatedT,
    CommandDataT,
]
UseCaseT: TypeAlias = UseCaseProtocol[
    CommandDataT,
    UseCaseResultT,
]
AdapterT: TypeAlias = AdapterProtocol[
    UseCaseResultT,
    RequestContextT,
    ResponseDataT,
]
DomainT: TypeAlias = CreateTaskDomainProtocol[
    ExerciseConfigProtocol,
    PresentationExerciseDomainResult,
]
OptionsDomainT: TypeAlias = CreateTaskDomainProtocol[
    ExerciseConfigProtocol,
    TestExerciseDomainResult,
]
RepositoryT: TypeAlias = RepositoryProtocol[
    object,
    object,
]
ServiceT: TypeAlias = UserSpecServiceProtocol[
    object,
    HasDomain[object],
]
TaskBuilderT: TypeAlias = SpecDtoBuilderProtocol[
    object,
    object,
    Any,
]

# =================================================
# Tested handler
# =================================================

HandlerT: TypeAlias = RequestHandler[
    RequestParamsT,
    RequestContextT,
    RequestDataT,
    ValidatedT,
    CommandDataT,
    DomainResultT,
    ResponseDataT,
]

# =================================================
# Resource type aliases
# =================================================

TranslationCandidates: TypeAlias = CandidatesT
