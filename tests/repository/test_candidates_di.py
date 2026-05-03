"""Exercise candidates repository tests."""

from typing import TypeAlias

import pytest

from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.users.models import Person
from contracts.schemas.base import NullDTO
from di import MainContainer
from interfaces.schemas.domain.exercise import TaskItem

_Translations: TypeAlias = list[TaskItem]
_Repository: TypeAlias = UserRepositoryProtocol[object, _Translations]


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
