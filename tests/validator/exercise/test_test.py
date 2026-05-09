"""Test exercise request validator tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import pytest

from apps.core.handlers.dto import RequestData
from apps.core.validators.request.exercise import ExerciseRequestValidator
from contracts.enums import ExerciseAction
from interfaces.schemas.validator.task import (
    ValidatedCheckTestAnswer,
    ValidatedCreateTask,
)

if TYPE_CHECKING:
    from apps.core.handlers.protocol import RequestDataProtocol
    from apps.core.validators.request.protocol import RequestValidatorProtocol
    from contracts.entity.domain.general import HasAction
    from interfaces.typed.exercise import TypedCheckTestAnswer, TypedCreateTask

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


# =================================================
# Fixtures
# =================================================


# Data
# ----


@pytest.fixture
def create_request_data() -> CreateRequestDataT:
    """Provide create exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CREATE_TASK,
        },
    )


@pytest.fixture
def check_request_data() -> CheckRequestDataT:
    """Provide check exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CHECK_ANSWER,
            'option_value': '3',
        },
    )


# Validated
# ---------


@pytest.fixture
def validated_create() -> ValidatedCreateT:
    """Provide the *create task* DTO validated request data."""
    return ValidatedCreateTask(
        action=ExerciseAction.CREATE_TASK,
    )


@pytest.fixture
def validated_check() -> ValidatedCreateT:
    """Provide the *check test answer* DTO validated request data."""
    return ValidatedCheckTestAnswer(
        action=ExerciseAction.CHECK_ANSWER,
        option_value=3,
    )


# Validator
# ---------


@pytest.fixture
def schema_registry() -> RegistryT:
    """Provide exercise action request validator schema registry."""
    return {
        ExerciseAction.CREATE_TASK: ValidatedCreateTask,
        ExerciseAction.CHECK_ANSWER: ValidatedCheckTestAnswer,
    }


@pytest.fixture
def validator(
    schema_registry: RegistryT,
) -> RequestValidatorProtocol[Any, Any]:
    """Provide test exercise request validator."""
    return ExerciseRequestValidator(schema_class_registry=schema_registry)


# =================================================
# Test
# =================================================


def test_validate_create_action_data(
    validator: CreateValidatorT,
    create_request_data: CreateRequestDataT,
    validated_create: ValidatedCreateT,
) -> None:
    """Test that create exercise action data validated."""
    # Act & Assert
    assert validator.validate(create_request_data) == validated_create


def test_validate_check_action_data(
    validator: CheckValidatorT,
    check_request_data: CheckRequestDataT,
    validated_check: ValidatedCheckT,
) -> None:
    """Test that create exercise action data validated."""
    # Act & Assert
    assert validator.validate(check_request_data) == validated_check
