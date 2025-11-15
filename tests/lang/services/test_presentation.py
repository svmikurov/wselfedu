"""Word study Presentation service tests."""

import uuid
from typing import TypedDict
from unittest.mock import Mock

import pytest

from apps.lang import services, types
from apps.lang.repos.abc import PresentationABC, TranslationRepoABC
from apps.lang.services.abc import WordStudyDomainABC


class Info(TypedDict):
    """Presentation case typed dict."""

    progress: int | None


class Case(TypedDict):
    """Presentation case typed dict."""

    case_uuid: uuid.UUID
    definition: str
    explanation: str
    info: Info


@pytest.fixture
def case_uuid() -> uuid.UUID:
    """Provide Word study presentation case."""
    return uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4')


@pytest.fixture
def mock_presentation_repo() -> Mock:
    """Mock Word study Presentation repository."""
    mock = Mock(spec=PresentationABC)
    return mock


@pytest.fixture
def mock_translation_repo() -> Mock:
    """Mock Translation repository."""
    mock = Mock(spec=TranslationRepoABC)
    return mock


@pytest.fixture
def mock_presentation_domain() -> Mock:
    """Mock Word study Presentation domain."""
    mock = Mock(spec=WordStudyDomainABC)
    return mock


@pytest.fixture
def service(
    mock_presentation_repo: Mock,
    mock_translation_repo: Mock,
    mock_django_cache_storage: Mock,
    mock_presentation_domain: Mock,
) -> services.WordPresentationService:
    """Provide Presentation service."""
    return services.WordPresentationService(
        word_repo=mock_presentation_repo,
        translation_repo=mock_translation_repo,
        case_storage=mock_django_cache_storage,
        domain=mock_presentation_domain,
    )


@pytest.fixture
def expected_case(
    case_uuid: uuid.UUID,
    presentation: types.PresentationDict,
) -> Case:
    """Provide Word study Presentation case."""
    return Case(
        case_uuid=case_uuid,
        definition=presentation['definition'],
        explanation=presentation['explanation'],
        info=Info(
            progress=presentation['progress'],
        ),
    )


@pytest.fixture
def params() -> Mock:
    """Provide Word study Presentation params."""
    return Mock(spec=types.WordParamsType)


class TestService:
    """Test Presentation service."""

    def test_get_presentation_case(
        self,
        case_uuid: uuid.UUID,
        presentation: types.PresentationDict,
        service: services.WordPresentationService,
        expected_case: Case,
    ) -> None:
        """Test get Presentation case."""
        # Act
        case = service._build_case(
            case_uuid=case_uuid,
            case_data=presentation,
        )

        # Assert
        assert case == expected_case
