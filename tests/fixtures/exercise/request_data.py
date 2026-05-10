"""Exercise fixtures."""

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.users.models import Person
from contracts.entity.domain.exercise.fields import HasExerciseAction
from contracts.enums.exercise import ExerciseAction
from contracts.schemas.request.exercise import ExerciseRequestDTO

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
