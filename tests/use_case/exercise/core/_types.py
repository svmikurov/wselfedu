"""Exercise use case types."""

from typing import Any, TypeAlias

from contracts.entity.domain.exercise import fields
from contracts.entity.domain.exercise.fields import HasExerciseAction
from interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
)
from ports.contract.infra.builder import TaskBuilderProtocol
from ports.contract.infra.reslover import ResolverProtocol
from ports.contract.infra.service import UserSpecServiceProtocol
from ports.contract.infra.spec import ExerciseSpecFactoryProtocol
from ports.contract.infra.storage.general import CommandStorageProtocol
from ports.contract.infra.use_case import UseCaseProtocol
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
ServiceT: TypeAlias = UserSpecServiceProtocol[
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
