"""Service specification create factory tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    ExerciseSpecDTO,
)
from interfaces.schemas.domain.exercise import TestAnswer
from interfaces.schemas.spec.exercise import CheckTestSpec
from kernel.spec import (
    CheckAnswerSpecFactory,
    CreateExerciseSpecFactory,
)
from tests.fixtures.exercise.lang.no_db.translations import (
    TRANSLATION_INDEX,
)

if TYPE_CHECKING:
    from interfaces.protocols.command.exercise import (
        CheckTestCommandProtocol,
        CreateTaskCommandProtocol,
    )
    from interfaces.schemas.domain.exercise import TestExerciseDomainResult
    from ports.contract.infra.spec import ExerciseSpecFactoryProtocol

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
        case=None,
    )


@pytest.mark.django_db
def test_check_test_answer_specification(
    check_test_command: CheckTestCommandProtocol,
    default_parameters: ExerciseParametersDTO,
    check_test_spec_factory: CreateTaskSpecFactoryT,
    create_translation_test_domain_result: TestExerciseDomainResult,
) -> None:
    """Test the check test task answer specification."""
    # Act & Assert
    assert check_test_spec_factory.create(
        check_test_command,
        default_parameters,
        create_translation_test_domain_result,
    ) == CheckTestSpec(
        answer=TestAnswer(
            option_value=TRANSLATION_INDEX,
        ),
        case=create_translation_test_domain_result,
    )
