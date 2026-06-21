"""Testing task use cases DI tests."""

from unittest.mock import Mock

from wse.application import commands, dto
from wse.di.application import ApplicationContainer
from wse.domain.protocols import Repository, Testable, UniqueLearnable

# The each task is identified by session ID value
SESSION_ID: str = 'test session'


def test_returns_created_task(
    learnables: tuple[UniqueLearnable, ...],
    container: ApplicationContainer,
) -> None:
    # Arrange
    create_cmd = commands.CreateTestingTask(session_id=SESSION_ID)

    mock_learnable_repo = Mock(spec=Repository)
    mock_learnable_repo.list.return_value = learnables

    mock_task_repo = Mock(spec=Repository)

    # Act
    with (
        container.repositories.learnable.override(mock_learnable_repo),
        container.repositories.task.override(mock_task_repo),
    ):
        use_case = container.create_testing()
        task_dto = use_case.execute(create_cmd)

        # Assert
        assert task_dto is not None
        assert task_dto.task is not None
        assert task_dto.session_id == SESSION_ID

        mock_learnable_repo.list.assert_called_once()

        saved_task = mock_task_repo.add.call_args[0][0]
        assert saved_task == task_dto


def test_returns_true_when_answer_correct(
    testing_task: Testable,
    container: ApplicationContainer,
) -> None:
    # Arrange
    check_cmd = commands.CheckTestingAnswer(
        session_id=SESSION_ID,
        answer_value=testing_task.question_value,
    )

    mock_repo = Mock(spec=Repository)
    mock_repo.get.return_value = dto.Task(
        task=testing_task, session_id=SESSION_ID
    )

    # Act
    with container.repositories.task.override(mock_repo):
        use_case = container.check_testing()
        result = use_case.execute(check_cmd)

        # Assert
        assert result is not None
        assert result.is_correct is True

        mock_repo.get.assert_called_once_with(SESSION_ID)


def test_returns_false_when_answer_incorrect(
    testing_task: Testable,
    container: ApplicationContainer,
) -> None:
    # Arrange
    check_cmd = commands.CheckTestingAnswer(
        session_id=SESSION_ID,
        answer_value=1 if testing_task.question_value != 1 else 2,
    )

    mock_repo = Mock(spec=Repository)
    mock_repo.get.return_value = dto.Task(
        task=testing_task, session_id=SESSION_ID
    )

    # Act
    with container.repositories.task.override(mock_repo):
        use_case = container.check_testing()
        result = use_case.execute(check_cmd)

        # Assert
        assert result is not None
        assert result.is_correct is False

        mock_repo.get.assert_called_once_with(SESSION_ID)
