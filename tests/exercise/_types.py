"""Exercise test types."""

from typing import Callable, Protocol

from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.protocol import RequestValidatorProtocol
from contracts.entity.domain.general import HasAction
from contracts.enums import ExerciseAction
from interfaces.typed.exercise import TypedCheckTestAnswer, TypedCreateTask


class RequestParams(Protocol):
    """Request parameters protocol."""


# Request data (protocols with generic typed dict)
type CreateRequestDataT = RequestDataProtocol[TypedCreateTask]
type CheckRequestDataT = RequestDataProtocol[TypedCheckTestAnswer]

# Validated data (protocols)
type ValidatedCreateT = HasAction[ExerciseAction]
type ValidatedCheckT = HasAction[ExerciseAction]

# Validator
type RegistryT = dict[
    ExerciseAction,
    Callable[..., HasAction[ExerciseAction]],
]
type CreateValidatorT = RequestValidatorProtocol[
    CreateRequestDataT,
    ValidatedCreateT,
]
type CheckValidatorT = RequestValidatorProtocol[
    CheckRequestDataT,
    ValidatedCheckT,
]
