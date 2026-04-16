"""Language use cases DI container test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.exercise.presentation.protocol import (
    PresentationCaseProtocol,
)
from apps.core.use_cases.protocol import UseCaseProtocol
from apps.core.validators.request.dto import ExerciseActionWebDTO
from apps.lang.models import EnglishTranslation

if TYPE_CHECKING:
    from apps.lang.di.use_case.container import UseCaseContainer
    from apps.users.models import Person
    from di import MainContainer


_UseCaseT = UseCaseProtocol[
    UserDataCommandProtocol[ExerciseActionWebDTO],
    PresentationCaseProtocol,
]
_CommandT = UserDataCommand[ExerciseActionWebDTO]


@pytest.fixture
def create_command(
    user: Person,
) -> UserDataCommand[ExerciseActionWebDTO]:
    """Provide request create exercise case command DTO fixture."""
    return UserDataCommand(
        user=user,
        data=ExerciseActionWebDTO(
            action=ExerciseProcessEnum.CREATE_CASE,
        ),
    )


@pytest.fixture
def use_cases(main_container: MainContainer) -> UseCaseContainer:
    """Provide lang app use cases DI container."""
    return main_container.lang.use_cases  # type: ignore


@pytest.fixture
def use_case(use_cases: UseCaseContainer) -> _UseCaseT:
    """Provide regular translation presentation use case fixture."""
    return use_cases.process_regular_translation_presentation()  # type: ignore


@pytest.mark.django_db
class TestRegularTranslationPresentationUseCaseStrategy:
    """Test regular translation presentation use case.

    Test exercise process use case strategy
    with translation presentation exercise.
    """

    def test_use_case_initialized(
        self,
        use_case: _UseCaseT,
    ) -> None:
        """Test that exercise use case has been initialized."""
        # Assert
        assert use_case

    def test_exercise_case_created(
        self,
        use_case: _UseCaseT,
        create_command: _CommandT,
        translations: list[EnglishTranslation],  # Populate DB
    ) -> None:
        """Test that new exercise case has been created."""
        # Act
        res = use_case.execute(command=create_command)

        # Assert
        assert res
