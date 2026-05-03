"""Exercise candidates repository test."""

import pytest

from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person
from contracts import NullProtocol
from contracts.schemas.base import NullDTO
from interfaces.schemas.domain.exercise import CandidateSchema

from .._types.resource import TranslationCandidates

_Repository = UserRepositoryProtocol[NullProtocol, list[CandidateSchema]]


@pytest.fixture
def repository() -> _Repository:
    """Provide translation candidates repository."""
    return UserTranslationsRepository(
        manager=EnglishTranslation.objects,
    )


@pytest.fixture
def candidates_db(
    translations: TranslationCandidates,
) -> TranslationCandidates:
    """Provide *translation* candidates for exercise."""
    return translations


class TestTranslationCandidatesRepository:
    """Translation candidates repository test."""

    def test_initialize_repository_success(
        self,
        repository: _Repository,
    ) -> None:
        """Repository initialized success."""
        assert repository is not None

    @pytest.mark.django_db
    def test_fetch_success(
        self,
        user: Person,
        repository: _Repository,
        candidates_db: TranslationCandidates,
    ) -> None:
        """Fetch translations test."""
        # Act
        candidates = repository.fetch(user, NullDTO())

        # Assert
        assert len(candidates) == len(candidates_db)

    @pytest.mark.django_db
    def test_fetch_not_owner(
        self,
        not_owner: Person,
        repository: _Repository,
        candidates_db: TranslationCandidates,
    ) -> None:
        """Fetch translations by not owner test."""
        # Act
        candidates = repository.fetch(not_owner, NullDTO())

        # Assert
        assert len(candidates) == 0

    @pytest.mark.django_db
    def test_has_candidate_interface(
        self,
        user: Person,
        repository: _Repository,
        candidates_db: TranslationCandidates,
    ) -> None:
        """Has exercise candidates interface test."""
        # Act
        candidates = repository.fetch(user, NullDTO())

        # Assert
        candidate = candidates[0]

        assert hasattr(candidate, 'define')
        assert candidate.define is not None

        assert hasattr(candidate, 'mean')
        assert candidate.mean is not None
