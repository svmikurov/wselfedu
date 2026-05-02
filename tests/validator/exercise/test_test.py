"""Test exercise request validator tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pytest

from apps.core.handlers.dto import RequestData
from apps.core.validators.request.exercise.create_task import (
    CreateExerciseTaskValidator,
)
from contracts.enums.exercise import ExerciseAction
from interfaces.schemas.validator.task import CreateTaskWebValidated

if TYPE_CHECKING:
    from apps.core.handlers.protocol import RequestDataProtocol
    from apps.core.validators.request.protocol import RequestValidatorProtocol
    from contracts.entity.domain.general import ActionTyped, HasAction

    type CreateDtoT = RequestDataProtocol[ActionTyped[ExerciseAction]]
    type ValidatedT = HasAction[ExerciseAction]
    type ValidatorT = RequestValidatorProtocol[CreateDtoT, ValidatedT]
    type RegistryT = dict[
        ExerciseAction,
        Callable[..., HasAction[ExerciseAction]],
    ]


@pytest.fixture
def create_exercise_dto() -> CreateDtoT:
    """Provide create exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CREATE_TASK,
        },
    )


@pytest.fixture
def schema_registry() -> RegistryT:
    """Provide exercise action request validator schema registry."""
    return {
        ExerciseAction.CREATE_TASK: CreateTaskWebValidated,
    }


@pytest.fixture
def validator(
    schema_registry: RegistryT,
) -> ValidatorT:
    """Provide test exercise request validator."""
    return CreateExerciseTaskValidator(schema_class_registry=schema_registry)


@pytest.fixture
def validated() -> ValidatedT:
    """Provide test exercise request validator."""
    return CreateTaskWebValidated(
        action=ExerciseAction.CREATE_TASK,
    )


def test_validate_create_action_data(
    validator: ValidatorT,
    create_exercise_dto: CreateDtoT,
    validated: ValidatedT,
) -> None:
    """Test that create exercise action data validated."""
    # Act & Assert
    assert validator.validate(create_exercise_dto) == validated
