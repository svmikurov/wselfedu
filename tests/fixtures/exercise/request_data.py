"""Exercise fixtures."""

import pytest

from apps.users.models import Person
from contracts.schemas.request.exercise import ExerciseRequestDTO
from ports.contract.entity.domain.exercise.fields import HasExerciseAction
from ports.contract.enums.exercise import ExerciseAction
from ports.interfaces.protocols.command import UserDataCommandProtocol
from ports.interfaces.schemas.command import UserDataCommand

CommandT = UserDataCommandProtocol[HasExerciseAction]


@pytest.fixture
def validated() -> HasExerciseAction:
    """Provide new case validated dto."""
    return ExerciseRequestDTO(
        action=ExerciseAction.CREATE_TASK,
    )


@pytest.fixture
def new_case_command(
    user: Person,
    validated: HasExerciseAction,
) -> CommandT:
    """Provide new case request fixture."""
    return UserDataCommand(
        user=user,
        data=validated,
    )
