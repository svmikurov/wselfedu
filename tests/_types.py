"""Exercise test types."""

from typing import Callable

from ports.contract.entity.domain.general import (
    HasAction,
)
from ports.contract.enums import ExerciseAction
from ports.contract.infra.validator import RequestValidatorProtocol
from ports.interfaces.protocols.handler.exercise import (
    CheckRequestDataT,
    CreateRequestDataT,
)
from ports.interfaces.protocols.validated.exercise import (
    ValidatedCheckTestRequestProtocol,
    ValidatedCreateTaskRequestProtocol,
)

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
