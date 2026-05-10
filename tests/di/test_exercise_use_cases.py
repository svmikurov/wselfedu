"""Language use cases DI container test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.lang.models import EnglishTranslation
from contracts.schemas.request.exercise import ExerciseRequestDTO
from interfaces.protocols.domain.exercise import PresentationTaskProtocol
from ports.contract.enums.exercise import ExerciseAction
from ports.contract.infra.use_case import UseCaseProtocol
from ports.interfaces.protocols.command import UserDataCommandProtocol
from ports.interfaces.schemas.command import UserDataCommand

if TYPE_CHECKING:
    from apps.lang.di.use_case.container import LangUseCaseContainer
    from apps.users.models import Person
    from di import MainContainer


_UseCaseT = UseCaseProtocol[
    UserDataCommandProtocol[ExerciseRequestDTO],
    PresentationTaskProtocol,
]
_CommandT = UserDataCommand[ExerciseRequestDTO]


@pytest.fixture
def create_command(
    user: Person,
) -> UserDataCommand[ExerciseRequestDTO]:
    """Provide request create exercise case command DTO fixture."""
    return UserDataCommand(
        user=user,
        data=ExerciseRequestDTO(
            action=ExerciseAction.CREATE_TASK,
        ),
    )


@pytest.fixture
def use_cases(main_container: MainContainer) -> LangUseCaseContainer:
    """Provide lang app use cases DI container."""
    return main_container.lang.use_cases  # type: ignore


@pytest.fixture
def use_case(use_cases: LangUseCaseContainer) -> _UseCaseT:
    """Provide regular translation presentation use case fixture."""
    return use_cases.regular_translation_presentation()  # type: ignore


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
