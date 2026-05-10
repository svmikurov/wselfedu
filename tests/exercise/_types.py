"""Exercise test types."""

from typing import Callable, Protocol

from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.protocol import RequestValidatorProtocol
from contracts.entity.domain.general import HasAction
from interfaces.protocols.validated.exercise import (
    ValidatedCheckTestRequestProtocol,
    ValidatedCreateTaskRequestProtocol,
)
from interfaces.typed.exercise import TypedCheckTestAnswer, TypedCreateTask
from ports.contract.enums import ExerciseAction


class RequestParams(Protocol):
    """Request parameters protocol."""


# Request data (protocols with generic typed dict)
type CreateRequestDataT = RequestDataProtocol[TypedCreateTask]
type CheckRequestDataT = RequestDataProtocol[TypedCheckTestAnswer]

# Validated data (protocols)
type ValidatedCreateT = ValidatedCreateTaskRequestProtocol
type ValidatedCheckT = ValidatedCheckTestRequestProtocol

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
