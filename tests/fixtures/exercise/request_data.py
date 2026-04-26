"""Exercise fixtures."""

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import HasExerciseAction
from apps.users.models import Person
from interfaces.enums.exercise import ExerciseAction
from interfaces.schemas.request.exercise import ExerciseRequestDTO

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
