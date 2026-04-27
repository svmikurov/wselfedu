"""Exercise service tests.

Test via Language app's english translation QuerySet
as exercise candidates.
"""

from unittest.mock import Mock

import pytest
from django.db.models import QuerySet

from apps.core.builders.exercise import case
from apps.core.services.exercise.generic import CreateExerciseService
from apps.lang.models import EnglishTranslation
from apps.users.models import Person
from interfaces import enums
from interfaces.schemas.domain.exercise import dtos
from interfaces.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
)
from tests._types import DomainT, RepositoryT, ServiceT, TaskBuilderT

_Candidates = QuerySet[EnglishTranslation]
_DomainT = DomainT
_ServiceT = ServiceT
_RepositoryT = RepositoryT
_TaskBuilderT = TaskBuilderT


@pytest.fixture
def candidates_db(
    translation_candidates_db: _Candidates,
) -> _Candidates:
    """Provide exercise candidates."""
    return translation_candidates_db


@pytest.fixture
def mock_candidates_repository(
    candidates_db: _Candidates,
) -> _RepositoryT:
    """Provide candidates repository mock."""
    mock = Mock(spec=_RepositoryT)
    mock.return_value.fetch = candidates_db
    return mock


@pytest.fixture
def mock_presentation_domain(
    candidates_db: _Candidates,
) -> _DomainT:
    """Provide presentation exercise domain mock."""
    mock = Mock(spec=_DomainT)
    mock.execute.return_value = dtos.PresentationExerciseDomainResult(
        status=enums.ExerciseStatus.NEW_TASK,
        exercise_kind=enums.ExerciseKind.PRESENTATION,
        option=candidates_db[0],
    )
    return mock


@pytest.fixture
def mock_test_domain(
    candidates_db: _Candidates,
) -> _DomainT:
    """Provide test exercise domain mock."""
    mock = Mock(spec=_DomainT)
    mock.execute.return_value = dtos.TestExerciseDomainResult(
        status=enums.ExerciseStatus.NEW_TASK,
        option_value=1,
        exercise_kind=enums.ExerciseKind.TEST,
        options=candidates_db,
    )
    return mock


@pytest.fixture
def service_result_builder() -> _TaskBuilderT:
    """Provide presentation exercise service's result builder."""
    return case.ExerciseCaseBuilder()  # type: ignore


@pytest.fixture
def presentation_service(
    mock_candidates_repository: Mock,
    mock_presentation_domain: Mock,
    service_result_builder: _TaskBuilderT,
) -> _ServiceT:
    """Provide presentation exercise service."""
    return CreateExerciseService(
        candidates_repository=mock_candidates_repository,
        domain=mock_presentation_domain,
        builder=service_result_builder,  # type: ignore
    )


@pytest.fixture
def test_service(
    mock_candidates_repository: Mock,
    mock_test_domain: Mock,
    service_result_builder: _TaskBuilderT,
) -> _ServiceT:
    """Provide test exercise service."""
    return CreateExerciseService(
        candidates_repository=mock_candidates_repository,
        domain=mock_test_domain,
        builder=service_result_builder,  # type: ignore
    )


@pytest.mark.django_db
def test_presentation_service_result_dto(
    mock_user: Person,
    exercise_params: ExerciseParametersDTO,
    presentation_service: _ServiceT,
) -> None:
    """Test the presentation domain result DTO."""
    # Act
    res = presentation_service.execute(mock_user, exercise_params)

    # Assert
    # - Case builder result DTO has fields
    assert hasattr(res, 'status')
    assert hasattr(res, 'domain')

    # - Case builder result DTO has nested fields
    assert hasattr(res.domain, 'exercise_kind')
    assert hasattr(res.domain, 'status')
    assert hasattr(res.domain, 'option')

    # - Presentation exercise domain result DTO is instance of
    assert isinstance(res, dtos.ExerciseCase)
    assert isinstance(res.domain, dtos.PresentationExerciseDomainResult)


@pytest.mark.django_db
def test_test_exercise_service_result_dto(
    mock_user: Person,
    exercise_params: ExerciseParametersDTO,
    test_service: _ServiceT,
) -> None:
    """Test the test domain result DTO."""
    # Act
    res = test_service.execute(mock_user, exercise_params)

    # Assert
    # - Case builder result DTO has fields
    assert hasattr(res, 'status')
    assert hasattr(res, 'domain')

    # - Case builder result DTO has nested fields
    assert hasattr(res.domain, 'exercise_kind')
    assert hasattr(res.domain, 'status')
    assert hasattr(res.domain, 'option_value')
    assert hasattr(res.domain, 'options')

    # - Presentation exercise domain result DTO is instance of
    assert isinstance(res, dtos.ExerciseCase)
    assert isinstance(res.domain, dtos.TestExerciseDomainResult)
