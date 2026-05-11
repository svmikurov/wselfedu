"""Exercise test types."""

from typing import Callable, Protocol

from ports.contract.entity.domain.general import (
    ActionTyped,
    HasAction,
    TypedOptionValue,
)
from ports.contract.enums import ExerciseAction
from ports.contract.infra.validator import RequestValidatorProtocol
from ports.interfaces.protocols.validated.exercise import (
    ValidatedCheckTestRequestProtocol,
    ValidatedCreateTaskRequestProtocol,
)
from ports.interfaces.protocols.web import RequestDataProtocol


class RequestParams(Protocol):
    """Request parameters protocol."""


class TypedCreateTask(
    ActionTyped[ExerciseAction],
):
    """Create task typed request data."""


class TypedCheckTestAnswer(
    ActionTyped[ExerciseAction],
    TypedOptionValue,
):
    """Check test answer typed request data."""


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
