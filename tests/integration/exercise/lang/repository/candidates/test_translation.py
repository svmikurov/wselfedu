"""Exercise candidates repository test."""

import pytest
from django.db.models import QuerySet

from apps.core.domains.null import NullDTO
from apps.core.domains.protocol import NullProtocol
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person

_Repository = UserRepositoryProtocol[
    NullProtocol,
    QuerySet[EnglishTranslation, EnglishTranslation],
]


@pytest.fixture
def repository() -> _Repository:
    """Provide translation candidates repository."""
    return UserTranslationsRepository(
        manager=EnglishTranslation.objects,
    )


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
        translations: list[EnglishTranslation],
    ) -> None:
        """Fetch translations test."""
        # Act
        candidates = repository.fetch(user, NullDTO())

        # Assert
        assert len(candidates) == len(translations)

    @pytest.mark.django_db
    def test_fetch_not_owner(
        self,
        not_owner: Person,
        repository: _Repository,
        translations: list[EnglishTranslation],
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
        translations: list[EnglishTranslation],  # Populate DB
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
