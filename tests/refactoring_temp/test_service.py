"""Presentation service tests."""

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from apps.core.storage import services as storage
from apps.lang import schemas
from apps.lang.domain import presentation as domain
from apps.lang.repositories import presentation as repository
from apps.lang.services import presentation

from .fixtures import EMPTY_PARAMETERS_DTO

if TYPE_CHECKING:
    from apps.lang import models

    # Data types
    type Translations = list[models.EnglishTranslation]


@pytest.fixture
def mock_repository() -> Mock:
    """Provide repository mock."""
    return Mock(spec=repository.EnglishTranslation)


@pytest.fixture
def mock_domain() -> Mock:
    """Provide presentation domain mock."""
    return Mock(spec=domain.PresentationDomain)


@pytest.fixture
def mock_storage() -> Mock:
    """Provide presentation case storage mock."""
    return Mock(spec=storage.TaskStorage)


@pytest.fixture
def service(
    mock_repository: Mock,
    mock_domain: Mock,
    mock_storage: Mock,
) -> presentation.PresentationService:
    """Provide presentation service."""
    return presentation.PresentationService(
        repository=mock_repository,
        domain=mock_domain,
        storage=mock_storage,
    )


class TestTranslationCount:
    """Translation count tests."""

    @pytest.mark.django_db
    def test_translation_count(
        self,
        service: presentation.PresentationService,
    ) -> None:
        """Apply translation order."""
        # Arrange
        _ = schemas.PresentationRequest(
            parameters=EMPTY_PARAMETERS_DTO,
            settings=schemas.SettingsModel(
                translation_order='to_native',
                word_count=3,
            ),
        )
