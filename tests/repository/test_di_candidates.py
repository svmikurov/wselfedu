"""Exercise candidates repository tests."""

from typing import TypeAlias

import pytest

from apps.users.models import Person
from di import MainContainer
from interfaces.schemas.domain.exercise import TaskItem
from ports.contract.infra.repository import RepositoryProtocol
from ports.interfaces.schemas.base import NullDTO

_Translations: TypeAlias = list[TaskItem]
_Repository: TypeAlias = RepositoryProtocol[object, _Translations]


@pytest.fixture
def repository(main_container: MainContainer) -> _Repository:
    """Provide DI translation candidates fixture."""
    return main_container.lang.repositories.translation_candidates()  # type: ignore


@pytest.mark.django_db
def test_fetch_resource_successfully(
    translations: _Translations,  # Populate DB
    user: Person,
    repository: _Repository,
) -> None:
    """Test that repository fetch resource called successfully."""
    # Act & assert
    assert repository.fetch(user, NullDTO()) == translations


@pytest.mark.django_db
def test_fetch_not_owner(
    not_owner: Person,
    repository: _Repository,
    translations: _Translations,  # Populate DB
) -> None:
    """Fetch translations by not owner test."""
    # Act
    candidates = repository.fetch(not_owner, NullDTO())

    # Assert
    assert len(candidates) == 0


@pytest.mark.django_db
def test_candidate_interface(
    user: Person,
    repository: _Repository,
    translations: _Translations,  # Populate DB
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

    assert hasattr(candidate, 'progress_value')
    assert candidate.progress_value is not None
