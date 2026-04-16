"""Exercise fixtures."""

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.exercise.protocol import HasExerciseProcessAction
from apps.core.validators.request.dto import ExerciseActionWebDTO
from apps.users.models import Person

CommandT = UserDataCommandProtocol[HasExerciseProcessAction]


@pytest.fixture
def validated() -> HasExerciseProcessAction:
    """Provide new case validated dto."""
    return ExerciseActionWebDTO(
        action=ExerciseProcessEnum.CREATE_CASE,
    )


@pytest.fixture
def new_case_command(
    user: Person,
    validated: HasExerciseProcessAction,
) -> CommandT:
    """Provide new case request fixture."""
    return UserDataCommand(
        user=user,
        data=validated,
    )
