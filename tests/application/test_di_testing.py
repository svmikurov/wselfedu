"""Testing task use cases DI tests."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

from tests.factories.model import TASK_SESSION_ID
from wse.application import dto

if TYPE_CHECKING:
    from wse.application.protocols import (
        CerateTestingCommandProto,
        CheckTestingCommandProto,
    )
    from wse.di.application import ApplicationContainer


class TestCreateTestingTaskUseCase:
    """Create testing task UseCase tests."""

    def test_creates_task_from_learnables(
        self,
        command_create_testing: CerateTestingCommandProto,
        container_with_mocks_for_task_execution: ApplicationContainer,
    ) -> None:
        # Arrange
        use_case = container_with_mocks_for_task_execution.create_testing()

        # Act
        task_dto = use_case.execute(command_create_testing)

        # Assert
        assert task_dto.session_id == TASK_SESSION_ID

    def test_created_task_have_been_saved(
        self,
        command_create_testing: CerateTestingCommandProto,
        mock_task_repo: Mock,
        container_with_mocks_for_task_execution: ApplicationContainer,
    ) -> None:
        # Arrange
        use_case = container_with_mocks_for_task_execution.create_testing()

        # Act
        task_dto = use_case.execute(command_create_testing)

        # Assert
        mock_task_repo.add.assert_called_once()
        mock_task_repo.get.assert_not_called()

        saved_task = mock_task_repo.add.call_args[0][0]
        assert saved_task == task_dto

        # - that saved task is DTO, not domain object
        assert isinstance(saved_task, dto.Task)


class TestCheckTestingAnswerUseCase:
    """Check testing answer UseCase tests."""

    def test_returns_true_when_answer_correct(
        self,
        command_check_testing_with_correct_answer: CheckTestingCommandProto,
        mock_task_repo: Mock,
        container_with_mocks_for_task_execution: ApplicationContainer,
    ) -> None:
        # Arrange
        use_case = container_with_mocks_for_task_execution.check_testing()

        # Act
        result = use_case.execute(command_check_testing_with_correct_answer)

        # Assert
        assert result is not None
        assert result.is_correct is True

        mock_task_repo.get.assert_called_once_with(TASK_SESSION_ID)

    def test_returns_false_when_answer_incorrect(
        self,
        mock_task_repo: Mock,
        command_check_testing_with_incorrect_answer: CheckTestingCommandProto,
        container_with_mocks_for_task_execution: ApplicationContainer,
    ) -> None:
        # Arrange
        use_case = container_with_mocks_for_task_execution.check_testing()

        # Act
        result = use_case.execute(command_check_testing_with_incorrect_answer)

        # Assert
        assert result is not None
        assert result.is_correct is False

        mock_task_repo.get.assert_called_once_with(TASK_SESSION_ID)
