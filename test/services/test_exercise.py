"""Test the exercise service."""

from unittest.mock import Mock

import pytest
from wse_exercises import SimpleMathExerciseConfig
from wse_exercises.core.mathem.base.exercise import SimpleMathTaskRequest
from wse_exercises.core.mathem.enums import Exercises

from services.exercise import SimpleMathExerciseService


@pytest.fixture
def mock_adding_exercise() -> Mock:
    """Adding exercise fixture."""
    exercise = Mock()
    exercise.create_task.return_value = Exercises.ADDING
    return exercise


@pytest.fixture
def mock_division_exercise() -> Mock:
    """Division exercise fixture."""
    exercise = Mock()
    exercise.create_task.return_value = Exercises.DIVISION
    return exercise


@pytest.fixture
def mock_adding_provider(mock_adding_exercise: Mock) -> Mock:
    """Adding exercise provider fixture."""
    provider = Mock()
    provider.return_value = mock_adding_exercise
    return provider


@pytest.fixture
def mock_division_provider(mock_division_exercise: Mock) -> Mock:
    """Division exercise provider fixture."""
    provider = Mock()
    provider.return_value = mock_division_exercise
    return provider


@pytest.fixture
def exercises_container(
    mock_adding_provider: Mock,
    mock_division_provider: Mock,
) -> Mock:
    """Division exercise provider fixture."""
    container = Mock()
    container.adding = mock_adding_provider
    container.division = mock_division_provider
    return container


@pytest.fixture
def service(exercises_container: Mock) -> SimpleMathExerciseService:
    """Service."""
    return SimpleMathExerciseService(exercises_container=exercises_container)


# Test data for parameterization
EXERCISE_TEST_CASES = [
    pytest.param(
        Exercises.ADDING,
        'mock_adding_exercise',
        Exercises.ADDING,
        id='adding_exercise',
    ),
    pytest.param(
        Exercises.DIVISION,
        'mock_division_exercise',
        Exercises.DIVISION,
        id='division_exercise',
    ),
]


@pytest.mark.parametrize(
    'exercise_name, mock_exercise_fixture, expected_result',
    EXERCISE_TEST_CASES,
)
def test_create_task_success(
    service: SimpleMathExerciseService,
    exercise_name: Exercises,
    mock_exercise_fixture: str,
    expected_result: str,
    request: pytest.FixtureRequest,
) -> None:
    """Test success create task service."""
    # Get the mock exercise fixture by name
    mock_exercise = request.getfixturevalue(mock_exercise_fixture)

    request_dto = SimpleMathTaskRequest(
        name=exercise_name,
        config=SimpleMathExerciseConfig(min_value=1, max_value=10),
    )

    task = service.create_task(request_dto)

    assert task == expected_result
    mock_exercise.create_task.assert_called_once()
