"""Exercise service tests.

Test via Language app's english translation QuerySet
as exercise candidates.
"""

from unittest.mock import Mock

import pytest

from apps.users.models import Person
from contracts.schemas.domain.exercise.flow import (
    ExerciseCase,
    PresentationTask,
    TestExerciseTask,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
)
from interfaces.protocols.domain.exercise import CandidatesT
from interfaces.schemas.domain.exercise import (
    PresentationExerciseDomainResult,
    TestExerciseDomainResult,
)
from kernel.formatter.exercise import PresentationFormatter, TestFormatter
from kernel.service.exercise import CreateExerciseService
from ports.contract import enums
from tests.types import DomainT, RepositoryT, ServiceT

_DomainT = DomainT
_ServiceT = ServiceT
_RepositoryT = RepositoryT
_TaskBuilderT = object


@pytest.fixture
def mock_candidates_repository(
    translations: CandidatesT,
) -> _RepositoryT:
    """Provide candidates repository mock."""
    mock = Mock(spec=_RepositoryT)
    mock.return_value.fetch = translations
    return mock


@pytest.fixture
def mock_presentation_domain(translations: CandidatesT) -> _DomainT:
    """Provide presentation exercise domain mock."""
    mock = Mock(spec=_DomainT)
    mock.execute.return_value = PresentationExerciseDomainResult(
        status=enums.ExerciseStatus.NEW_TASK,
        exercise_kind=enums.ExerciseKind.PRESENTATION,
        item=translations[0],  # type: ignore
    )
    return mock


@pytest.fixture
def mock_test_domain(translations: CandidatesT) -> _DomainT:
    """Provide test exercise domain mock."""
    mock = Mock(spec=_DomainT)
    mock.execute.return_value = TestExerciseDomainResult(
        status=enums.ExerciseStatus.NEW_TASK,
        question_option_value=1,
        exercise_kind=enums.ExerciseKind.TEST,
        items=translations,  # type: ignore
    )
    return mock


@pytest.fixture
def presentation_formatter() -> _TaskBuilderT:
    """Provide presentation exercise domain result formatter."""
    return PresentationFormatter()


@pytest.fixture
def test_formatter() -> _TaskBuilderT:
    """Provide test exercise domain result formatter."""
    return TestFormatter()


@pytest.fixture
def presentation_service(
    mock_candidates_repository: Mock,
    mock_presentation_domain: Mock,
    presentation_formatter: _TaskBuilderT,
) -> _ServiceT:
    """Provide presentation exercise service."""
    return CreateExerciseService(
        candidates_repository=mock_candidates_repository,
        domain=mock_presentation_domain,
        formatter=presentation_formatter,  # type: ignore
    )


@pytest.fixture
def test_service(
    mock_candidates_repository: Mock,
    mock_test_domain: Mock,
    test_formatter: _TaskBuilderT,
) -> _ServiceT:
    """Provide test exercise service."""
    return CreateExerciseService(
        candidates_repository=mock_candidates_repository,
        domain=mock_test_domain,
        formatter=test_formatter,  # type: ignore
    )


@pytest.mark.django_db
def test_presentation_service_result_dto(
    mock_user: Person,
    exercise_params: ExerciseParametersDTO,
    presentation_service: _ServiceT,
) -> None:
    """Test the presentation domain result DTO."""
    # Act
    case = presentation_service.execute(mock_user, exercise_params)

    # Assert
    # - Case builder result DTO has fields
    assert hasattr(case, 'status')
    assert hasattr(case, 'domain')

    # - Case builder result DTO has nested fields
    assert hasattr(case.domain, 'question_text')
    assert hasattr(case.domain, 'answer_text')
    assert hasattr(case.domain, 'progress_value')

    # - Presentation exercise domain result DTO is instance of
    assert isinstance(case, ExerciseCase)
    assert isinstance(case.domain, PresentationTask)


@pytest.mark.django_db
def test_test_exercise_service_result_dto(
    mock_user: Person,
    exercise_params: ExerciseParametersDTO,
    test_service: _ServiceT,
) -> None:
    """Test the test domain result DTO."""
    # Act
    case = test_service.execute(mock_user, exercise_params)

    # Assert
    # - Case builder result DTO has fields
    assert hasattr(case, 'status')
    assert hasattr(case, 'domain')

    # - Case builder result DTO has nested fields
    assert hasattr(case.domain, 'question_text')
    assert hasattr(case.domain, 'question_option_value')
    assert hasattr(case.domain, 'items')

    # - Presentation exercise domain result DTO is instance of
    assert isinstance(case, ExerciseCase)
    assert isinstance(case.domain, TestExerciseTask)
