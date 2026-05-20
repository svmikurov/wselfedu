"""Exercise fixtures."""

import pytest

from apps.users.models import Person
from ports.contract.entity.domain.exercise import HasExerciseAction
from ports.contract.enums.exercise import ExerciseAction
from ports.interfaces.protocols.command.assembler import (
    UserDataCommandProtocol,
)
from ports.interfaces.schemas.command import UserDataCommand
from ports.interfaces.schemas.handler import CreateTaskSchema

CommandT = UserDataCommandProtocol[HasExerciseAction]


@pytest.fixture
def validated() -> HasExerciseAction:
    """Provide new case validated dto."""
    return CreateTaskSchema(
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
