"""Exercise test types."""

from typing import Callable, Protocol

from ports.contract.entity.domain.general import (
    HasAction,
)
from ports.contract.enums import ExerciseAction
from ports.contract.infra.validator import RequestValidatorProtocol
from ports.interfaces.protocols.validated.exercise import (
    ValidatedCheckTestRequestProtocol,
    ValidatedCreateTaskRequestProtocol,
)
from ports.interfaces.protocols.web import RequestDataProtocol
from ports.interfaces.request.web.exercise import (
    CheckTestData,
    CreateTaskData,
    UpdateProgressData,
)


class RequestParams(Protocol):
    """Request parameters protocol."""


# Request data (protocols with generic typed dict)
type CreateRequestDataT = RequestDataProtocol[CreateTaskData]
type CheckRequestDataT = RequestDataProtocol[CheckTestData]
type UpdateProgressRequestDataT = RequestDataProtocol[UpdateProgressData]

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
