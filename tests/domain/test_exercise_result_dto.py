"""Exercise domain tests.

Test via Language app's english translation QuerySet
as exercise candidates.
"""

import pytest

from apps.core.domains.exercise import PresentationDomain, TestDomain
from contracts.schemas.domain.exercise.params import ExerciseParametersDTO
from interfaces.protocols.domain.exercise import CandidatesT
from interfaces.schemas.domain.exercise import (
    PresentationExerciseDomainResult,
    TaskItem,
    TestExerciseDomainResult,
)
from kernel.domain.exercise import CandidatesSelector
from tests.types import DomainT, OptionsDomainT

_DomainT = DomainT
_OptionsDomainT = OptionsDomainT


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
    translations: CandidatesT,
    presentation_domain: _DomainT,
    exercise_params: ExerciseParametersDTO,
) -> None:
    """Test the presentation domain DTO."""
    # Act
    res = presentation_domain.execute(translations, exercise_params.conf)

    # Assert
    # - Domain result DTO has fields
    assert hasattr(res, 'exercise_kind')
    assert hasattr(res, 'status')
    assert hasattr(res, 'item')  # <--- Note: Has one option

    # - Option field value is `CandidateSchema` instance
    assert isinstance(res.item, TaskItem)

    # - Presentation exercise domain result DTO is instance of
    assert isinstance(res, PresentationExerciseDomainResult)


@pytest.mark.django_db
def test_test_exercise_domain_result(
    translations: CandidatesT,
    test_exercise_domain: _OptionsDomainT,
    exercise_params: ExerciseParametersDTO,
) -> None:
    """Test the test exercise domain DTO."""
    # Act
    res = test_exercise_domain.execute(translations, exercise_params.conf)

    # Assert
    # - Domain result DTO has fields
    assert hasattr(res, 'exercise_kind')
    assert hasattr(res, 'status')
    assert hasattr(res, 'items')  # <--- Note: Has some options

    # - Options field is `CandidateSchema` instance
    assert isinstance(res.items, list)
    assert isinstance(res.items[0], TaskItem)

    # - Test exercise domain result DTO is instance of
    assert isinstance(res, TestExerciseDomainResult)
