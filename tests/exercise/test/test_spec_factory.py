"""Service specification create factory tests."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.core.factories import (
    CheckAnswerSpecFactory,
    CreateExerciseSpecFactory,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    ExerciseSpecDTO,
)

if TYPE_CHECKING:
    from apps.core.factories.protocol import ExerciseSpecFactoryProtocol
    from interfaces.protocols.command.exercise import (
        CheckTestCommandProtocol,
        CreateTaskCommandProtocol,
    )

    type CreateTaskSpecFactoryT = ExerciseSpecFactoryProtocol[
        object, object, object, object
    ]

    type CheckTaskSpecFactoryT = ExerciseSpecFactoryProtocol[
        object, object, object, object
    ]

# =================================================
# Fixtures
# =================================================

# Specification factory attributes
# --------------------------------


@pytest.fixture
def default_parameters() -> ExerciseParametersDTO:
    """Provide default user's exercise configuration."""
    return ExerciseParametersDTO()


# Specification factory
# ---------------------


@pytest.fixture
def create_task_spec_factory() -> CreateTaskSpecFactoryT:
    """Provide the create task service specification."""
    return CreateExerciseSpecFactory()  # type: ignore


@pytest.fixture
def check_test_spec_factory() -> CheckTaskSpecFactoryT:
    """Provide the check test answer service specification."""
    return CheckAnswerSpecFactory()  # type: ignore


# =================================================
# Tests
# =================================================


@pytest.mark.django_db
def test_create_task_specification(
    create_task_command: CreateTaskCommandProtocol,
    default_parameters: ExerciseParametersDTO,
    create_task_spec_factory: CreateTaskSpecFactoryT,
    create_task_spec: object,
) -> None:
    """Test the create exercise task specification."""
    # Act & Assert
    assert create_task_spec_factory.create(
        create_task_command,
        default_parameters,
        None,  # Create specification without existing case
    ) == ExerciseSpecDTO(
        existing_case=None,
    )


@pytest.mark.django_db
def test_check_test_answer_specification(
    check_test_command: CheckTestCommandProtocol,
    default_parameters: ExerciseParametersDTO,
    check_test_spec_factory: CreateTaskSpecFactoryT,
    mock_existing_case: Mock,
) -> None:
    """Test the check test task answer specification."""
    # Act & Assert
    assert check_test_spec_factory.create(
        check_test_command,
        default_parameters,
        mock_existing_case,
    ) == ExerciseSpecDTO(
        existing_case=mock_existing_case,
    )
