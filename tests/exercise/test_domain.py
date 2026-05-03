"""Exercise domain tests.

Test via Language app's english translation QuerySet
as exercise candidates.
"""

import pytest
from django.db.models import QuerySet

from apps.core.domains.exercise.deps.selector import CandidatesSelector
from apps.core.domains.exercise.presentation.impl import PresentationDomain
from apps.core.domains.exercise.test.impl import TestDomain
from apps.lang.models import EnglishTranslation
from contracts.schemas.domain.exercise import flow
from contracts.schemas.domain.exercise.params import ExerciseParametersDTO
from interfaces.protocols.domain.exercise import Candidates
from interfaces.schemas.domain.exercise import CandidateSchema
from tests._types import DomainT, OptionsDomainT

_CandidatesT = QuerySet[EnglishTranslation]
_DomainT = DomainT
_OptionsDomainT = OptionsDomainT


@pytest.fixture
def candidates_db(
    translation_candidates_db: _CandidatesT,
) -> _CandidatesT:
    """Provide exercise candidates."""
    return translation_candidates_db


@pytest.fixture
def presentation_domain() -> _DomainT:
    """Provide presentation domain."""
    return PresentationDomain(selector=CandidatesSelector())  # type: ignore


@pytest.fixture
def test_exercise_domain() -> _DomainT:
    """Provide test exercise domain."""
    return TestDomain(selector=CandidatesSelector())  # type: ignore


@pytest.mark.django_db
def test_presentation_domain_result(
    candidates_db: Candidates,
    presentation_domain: _DomainT,
    exercise_params: ExerciseParametersDTO,
) -> None:
    """Test the presentation domain DTO."""
    # Act
    res = presentation_domain.execute(candidates_db, exercise_params.conf)

    # Assert
    # - Domain result DTO has fields
    assert hasattr(res, 'exercise_kind')
    assert hasattr(res, 'status')
    assert hasattr(res, 'option')  # <--- Note: Has one option

    # - Option field value is `CandidateSchema` instance
    assert isinstance(res.option, CandidateSchema)

    # - Presentation exercise domain result DTO is instance of
    assert isinstance(res, flow.PresentationExerciseDomainResult)


@pytest.mark.django_db
def test_test_exercise_domain_result(
    candidates_db: Candidates,
    test_exercise_domain: _OptionsDomainT,
    exercise_params: ExerciseParametersDTO,
) -> None:
    """Test the test exercise domain DTO."""
    # Act
    res = test_exercise_domain.execute(candidates_db, exercise_params.conf)

    # Assert
    # - Domain result DTO has fields
    assert hasattr(res, 'exercise_kind')
    assert hasattr(res, 'status')
    assert hasattr(res, 'options')  # <--- Note: Has some options

    # - Options field is `CandidateSchema` instance
    assert isinstance(res.options, list)
    assert isinstance(res.options[0], CandidateSchema)

    # - Test exercise domain result DTO is instance of
    assert isinstance(res, flow.TestExerciseDomainResult)
