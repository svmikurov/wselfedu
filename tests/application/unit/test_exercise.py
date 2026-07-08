"""Exercise use case test."""

from unittest.mock import Mock

import pytest

from tests.factories.model import (
    CORRECT_ANSWER_OPTION_VALUE,
    INCORRECT_ANSWER_OPTION_VALUE,
    TASK_SESSION_ID,
    create_testing_task,
    create_testing_task_dto,
    get_learnables,
)
from wse.application.commands import CheckTestingAnswer, CreateTestingTask
from wse.application.protocols import (
    CheckTestingCommandProto,
    CreateTaskCommandProto,
    Executable,
    HasExerciseAction,
    TaskDtoProto,
)
from wse.application.use_cases import ExerciseUseCaseStrategy
from wse.domain import enums
from wse.domain.protocols import Testable

UseCaseT = Executable[
    HasExerciseAction[enums.ExerciseAction],
    TaskDtoProto[Testable],
]


###################################################
# Use cases
###################################################


@pytest.fixture
def testing_task_dto() -> TaskDtoProto[Testable]:
    """Provide the testing task."""
    task = create_testing_task(get_learnables())
    return create_testing_task_dto(task)


@pytest.fixture
def create_task_use_case(testing_task_dto: TaskDtoProto[Testable]) -> UseCaseT:
    """Provide the create task use case mock."""
    mock = Mock(spec=Executable)
    mock.execute.return_value = testing_task_dto
    return mock


@pytest.fixture
def check_task_use_case() -> UseCaseT:
    """Provide the check task answer use case mock."""
    return Mock(spec=Executable)


@pytest.fixture
def use_case_registry(
    create_task_use_case: UseCaseT,
    check_task_use_case: UseCaseT,
) -> dict[enums.ExerciseAction, UseCaseT]:
    """Provide the exercise use case registry."""
    return {
        enums.ExerciseAction.CREATE_TASK: create_task_use_case,
        enums.ExerciseAction.CHECK_ANSWER: check_task_use_case,
    }


@pytest.fixture
def exercise_use_case_strategy(
    use_case_registry: dict[enums.ExerciseAction, UseCaseT],
) -> ExerciseUseCaseStrategy:
    """Provide the exercise use case strategy."""
    return ExerciseUseCaseStrategy(
        use_case_registry=use_case_registry,
    )


###################################################
# Use case commands
###################################################


@pytest.fixture
def create_task_command() -> CreateTaskCommandProto:
    """Provide the create task command."""
    return CreateTestingTask(
        session_id=TASK_SESSION_ID,
    )


@pytest.fixture
def check_correct_answer_command() -> CheckTestingCommandProto:
    """Provide the check task command with correct answer."""
    return CheckTestingAnswer(
        session_id=TASK_SESSION_ID,
        answer_value=CORRECT_ANSWER_OPTION_VALUE,
    )


@pytest.fixture
def check_incorrect_answer_command() -> CheckTestingCommandProto:
    """Provide the check task command with incorrect answer."""
    return CheckTestingAnswer(
        session_id=TASK_SESSION_ID,
        answer_value=INCORRECT_ANSWER_OPTION_VALUE,
    )


###################################################
# Tests
###################################################


def test_should_provide_task_when_no_active_task(
    exercise_use_case_strategy: Executable[
        CreateTaskCommandProto,
        TaskDtoProto[Testable],
    ],
    create_task_use_case: Mock,
    create_task_command: CreateTaskCommandProto,
    testing_task: Testable,
) -> None:
    # Act
    result = exercise_use_case_strategy.execute(create_task_command)

    # Assert
    create_task_use_case.execute.assert_called_once_with(create_task_command)
    assert result.task == testing_task


@pytest.mark.skip(reason='Not implemented yet')
def test_should_return_active_task_if_exists() -> None: ...


def test_should_advance_to_next_question_on_correct_answer(
    exercise_use_case_strategy: Executable[
        CreateTaskCommandProto,
        TaskDtoProto[Testable],
    ],
    check_task_use_case: Mock,
    check_correct_answer_command: CheckTestingCommandProto,
    testing_task: Testable,
) -> None:
    # Act
    result = exercise_use_case_strategy.execute(check_correct_answer_command)

    # Assert
    check_task_use_case.execute.assert_called_once_with(
        check_correct_answer_command
    )
    assert result.task == testing_task


@pytest.mark.skip(reason='Not implemented yet')
def test_should_show_explanation_on_incorrect_answer() -> None: ...
