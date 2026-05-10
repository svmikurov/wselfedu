"""Exercise use case types."""

from typing import Any, TypeAlias

from apps.core.resolvers.protocol import ResolverProtocol
from apps.core.services.protocol import UserServiceProtocol
from apps.core.storages.services.protocol import CommandStorageProtocol
from apps.core.use_cases.protocol import UseCaseProtocol
from contracts.entity.domain.exercise import fields
from contracts.entity.domain.exercise.fields import HasExerciseAction
from interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
)
from ports.contract.infra.builder import TaskBuilderProtocol
from ports.contract.infra.spec import ExerciseSpecFactoryProtocol
from ports.interfaces.protocols.command import UserDataCommandProtocol

# =================================================
# DTOs
# =================================================

CommandT: TypeAlias = UserDataCommandProtocol[HasExerciseAction]
"""Request command DTO.
"""
Params: TypeAlias = Any
"""Exercise parameters DTO.
"""
SpecT: TypeAlias = Any
"""Specification DTO for exercise case perform.
"""
CaseT: TypeAlias = fields.HasExerciseStatus
"""Exercise perform result DTO.
"""
ResultT: TypeAlias = fields.HasExerciseStatus
"""Use case result DTO.
"""


# =================================================
# Use case dependencies
# =================================================

StorageT: TypeAlias = CommandStorageProtocol[
    CommandT,
    CaseT,
]
ResolverT: TypeAlias = ResolverProtocol[
    CommandT,
    Params,
]
SpecFactoryT: TypeAlias = ExerciseSpecFactoryProtocol[
    CommandT,
    ExerciseParametersProtocol,
    CaseT | None,
    SpecT,
]
ServiceT: TypeAlias = UserServiceProtocol[
    SpecT,
    Any,
]
BuilderT: TypeAlias = TaskBuilderProtocol[
    Any,
    ExerciseConfigProtocol,
    ResultT,
]


# =================================================
# Use case
# =================================================

UseCaseT: TypeAlias = UseCaseProtocol[
    CommandT,
    ResultT,
]
