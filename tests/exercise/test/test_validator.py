"""Test exercise request validator tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from interfaces.schemas.validator.task import (
    ValidatedCheckTestAnswer,
    ValidatedCreateTask,
)
from kernel.validator.request.exercise import ExerciseRequestValidator
from ports.contract.enums import ExerciseAction

if TYPE_CHECKING:
    from ports.contract.infra.validator import RequestValidatorProtocol

    from .._types import (
        CheckRequestDataT,
        CheckValidatorT,
        CreateRequestDataT,
        CreateValidatorT,
        RegistryT,
        ValidatedCheckT,
        ValidatedCreateT,
    )

# =================================================
# Fixtures
# =================================================


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
# Tests
# =================================================


def test_validate_create_action_data(
    validator: CreateValidatorT,
    create_task_request_data: CreateRequestDataT,
    validated_create: ValidatedCreateT,
) -> None:
    """Test that create exercise action data validated."""
    # Act & Assert
    assert validator.validate(create_task_request_data) == validated_create


def test_validate_check_action_data(
    validator: CheckValidatorT,
    check_test_answer_request_data: CheckRequestDataT,
    validated_check: ValidatedCheckT,
) -> None:
    """Test that create exercise action data validated."""
    # Act & Assert
    assert (
        validator.validate(check_test_answer_request_data) == validated_check
    )
