"""Exercise process response adapter test."""

from typing import Any

import pytest

from apps.core.adapters.exercise.process import ExerciseProcessAdapter
from apps.core.adapters.exercise.protocol import ExerciseProcessAdapterProtocol
from apps.core.assemblers.command import UserDataCommand
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.dto import (
    ExerciseParametersDTO,
    ExerciseSpecDTO,
)
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.exercise.protocol import (
    HasExerciseProcessAction,
)
from apps.core.validators.request.dto import ExerciseActionWebDTO
from apps.users.models import Person

type CaseT = Any

_Adapter = ExerciseProcessAdapterProtocol[
    UserDataCommandProtocol[HasExerciseProcessAction],
    ExerciseParametersDTO,
    CaseT | None,
    ExerciseSpecDTO[CaseT],
]


@pytest.fixture
def validated() -> ExerciseActionWebDTO:
    """Provide validated request DTO fixture."""
    return ExerciseActionWebDTO(
        action=ExerciseProcessEnum.CREATE_CASE,
    )


@pytest.fixture
def command(
    user: Person,
    validated: ExerciseActionWebDTO,
) -> UserDataCommand[ExerciseActionWebDTO]:
    """Provide request command DTO fixture."""
    return UserDataCommand(
        user=user,
        data=validated,
    )


@pytest.fixture
def params() -> ExerciseParametersDTO:
    """Provide exercise parameters DTO fixture."""
    return ExerciseParametersDTO()


@pytest.fixture
def adapter() -> ExerciseProcessAdapter[CaseT]:
    """Provide response adapter fixture."""
    return ExerciseProcessAdapter()


class TestExerciseAdapter:
    """Exercise process response adapter test."""

    @pytest.mark.django_db
    def test_success(
        self,
        adapter: _Adapter,
        command: UserDataCommandProtocol[HasExerciseProcessAction],
        params: ExerciseParametersDTO,
        existing_case: None = None,
    ) -> None:
        """Test adapt."""
        # Act
        spec = adapter.adapt(command, params, existing_case)

        # Assert
        assert spec
        assert spec.conditions == params.conditions
        assert spec.conf == params.conf
        assert spec.settings == params.settings
        assert spec.existing_case is None
