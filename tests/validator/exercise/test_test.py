"""Test exercise request validator tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.core.handlers.dto import RequestData
from apps.core.validators.request.exercise.create_task import (
    CreateExerciseTaskValidator,
)
from interfaces.enums.exercise import ExerciseAction
from interfaces.schemas.request.exercise import ExerciseRequestDTO

if TYPE_CHECKING:
    from apps.core.handlers.protocol import RequestDataProtocol
    from apps.core.validators.request.protocol import RequestValidatorProtocol
    from interfaces.entity.domain.general import (
        ActionTyped,
        HasAction,
    )

    type CreateDtoT = RequestDataProtocol[ActionTyped]
    type ValidatorT = RequestValidatorProtocol[CreateDtoT, ValidatedT]
    type ValidatedT = HasAction[ExerciseAction]


@pytest.fixture
def create_exercise_dto() -> CreateDtoT:
    """Provide create exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': 'create_task',
        },
    )


@pytest.fixture
def validator() -> ValidatorT:
    """Provide test exercise request validator."""
    return CreateExerciseTaskValidator()


@pytest.fixture
def validated() -> ValidatedT:
    """Provide test exercise request validator."""
    return ExerciseRequestDTO(
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
