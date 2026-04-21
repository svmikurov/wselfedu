"""Test exercise request validator tests."""

from typing import TypeAlias

import pytest

from apps.core.contracts.request.protocol import HasAction
from apps.core.contracts.request.web.exercise import CreateExerciseRequestDTO
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.handlers.dto import RequestData
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.exercise.test import TestExerciseWebValidator
from apps.core.validators.request.protocol import (
    ExerciseProcessAction,
    RequestValidatorProtocol,
)

CreateRequestDtoT: TypeAlias = RequestDataProtocol[ExerciseProcessAction]
ValidatedT: TypeAlias = HasAction[ExerciseProcessEnum]
ValidatorT: TypeAlias = RequestValidatorProtocol[
    CreateRequestDtoT,
    ValidatedT,
]


@pytest.fixture
def create_request_dto() -> CreateRequestDtoT:
    """Provide create exercise request data."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseProcessEnum.CREATE_CASE,
        },
    )


@pytest.fixture
def validator() -> ValidatorT:
    """Provide test exercise request validator."""
    return TestExerciseWebValidator()


@pytest.fixture
def validated() -> ValidatedT:
    """Provide test exercise request validator."""
    return CreateExerciseRequestDTO(
        action=ExerciseProcessEnum.CREATE_CASE,
    )


def test_validate_successfully(
    validator: ValidatorT,
    create_request_dto: CreateRequestDtoT,
    validated: ValidatedT,
) -> None:
    """Test that create exercise request data validated."""
    # Act & Assert
    assert validator.validate(create_request_dto) == validated
