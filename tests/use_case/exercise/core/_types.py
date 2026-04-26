"""Exercise use case types."""

from typing import Any, TypeAlias

from apps.core.adapters.exercise.protocol import ExerciseProcessAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
    ExerciseProcessResultProtocol,
    HasExerciseAction,
)
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.resolvers.protocol import ResolverProtocol
from apps.core.services.protocol import UserServiceProtocol
from apps.core.storages.services.protocol import CommandStorageProtocol
from apps.core.use_cases.protocol import UseCaseProtocol
from interfaces.entity.domain.exercise import fields

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
AdapterT: TypeAlias = ExerciseProcessAdapterProtocol[
    CommandT,
    ExerciseParametersProtocol,
    CaseT | None,
    SpecT,
]
ServiceT: TypeAlias = UserServiceProtocol[
    SpecT,
    ExerciseProcessResultProtocol[CaseT],
]
BuilderT: TypeAlias = TaskBuilderProtocol[
    ExerciseProcessResultProtocol[CaseT],
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
