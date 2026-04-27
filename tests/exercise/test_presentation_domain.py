"""Exercise domain tests.

Test via Language app's english translation QuerySet
as exercise candidates.
"""

import pytest
from django.db.models import Model, QuerySet

from apps.core.domains.exercise.deps.selector import CandidatesSelector
from apps.core.domains.exercise.presentation.impl import PresentationDomain
from apps.lang.models import EnglishTranslation
from interfaces.entity.domain.exercise.fields import Candidates
from interfaces.schemas.domain.exercise.dtos import (
    PresentationExerciseDomainResult,
)
from interfaces.schemas.domain.exercise.params import ExerciseConfigDTO
from tests._types import DomainT

_Candidates = QuerySet[EnglishTranslation]
_Domain = DomainT


@pytest.fixture
def candidates_db(
    translation_candidates_db: _Candidates,
) -> _Candidates:
    """Provide presentation exercise candidates."""
    return translation_candidates_db


@pytest.fixture
def presentation_domain() -> _Domain:
    """Provide presentation domain."""
    return PresentationDomain(selector=CandidatesSelector())  # type: ignore


@pytest.mark.django_db
def test_presentation_domain_result(
    candidates_db: Candidates,
    presentation_domain: _Domain,
) -> None:
    """Test the presentation domain result."""
    # Act
    res = presentation_domain.execute(candidates_db, ExerciseConfigDTO())

    # Assert
    # - Domain result DTO has fields
    assert hasattr(res, 'exercise_kind')
    assert hasattr(res, 'status')
    assert hasattr(res, 'option')

    # - Exercise's option is Django ORM model instance
    #   if candidates is QuerySet
    assert isinstance(res.option, Model)

    # - Domain result DTO type
    assert isinstance(res, PresentationExerciseDomainResult)
