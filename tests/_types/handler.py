"""Handler dependencies type aliases."""

from typing import Any, TypeAlias

from apps.core.adapters.response.protocol import AdapterProtocol
from apps.core.assemblers.protocol import AssemblerProtocol
from apps.core.builders.protocol import SpecDtoBuilderProtocol
from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseDomainProtocol,
)
from apps.core.handlers.generic import RequestHandler
from apps.core.handlers.protocol import (
    RequestContextProtocol,
    RequestDataProtocol,
)
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.core.services.exercise.protocol import ExerciseServiceProtocol
from apps.core.use_cases.protocol import UseCaseProtocol
from apps.core.validators.request.protocol import RequestValidatorProtocol
from apps.lang.models import EnglishTranslation
from contracts.entity.domain.exercise.fields import Candidates, HasDomain
from contracts.entity.general import NullProtocol
from contracts.schemas.domain.exercise.flow import (
    PresentationExerciseDomainResult,
    TestExerciseDomainResult,
)

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
AssemblerT: TypeAlias = AssemblerProtocol[
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
DomainT: TypeAlias = ExerciseDomainProtocol[
    ExerciseConfigProtocol,
    PresentationExerciseDomainResult[EnglishTranslation],
]
OptionsDomainT: TypeAlias = ExerciseDomainProtocol[
    ExerciseConfigProtocol,
    TestExerciseDomainResult[EnglishTranslation],
]
RepositoryT: TypeAlias = UserRepositoryProtocol[
    object,
    object,
]
ServiceT: TypeAlias = ExerciseServiceProtocol[
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

TranslationCandidates: TypeAlias = Candidates
