"""Word study Presentation service tests."""

import uuid
from typing import TypedDict
from unittest.mock import Mock

import pytest

from apps.core.storage.clients import DjangoCache
from apps.lang import services, types
from apps.lang.repos.abc import PresentationABC
from apps.lang.services.study import WordStudyDomain


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
def mock_presentation_repo(
    presentation: types.PresentationDict,
) -> Mock:
    """Mock Word study Presentation repository."""
    mock = Mock(spec=PresentationABC)
    mock.get_candidates.return_value = types.WordStudyParams(
        translation_ids=[1],
    )
    mock.get_case.return_value = presentation
    return mock


@pytest.fixture
def mock_django_cache_storage(
    case_uuid: uuid.UUID,
) -> Mock:
    """Mock Django cache storage fixture."""
    mock = Mock(spec=DjangoCache)
    mock.set.return_value = case_uuid
    return mock


@pytest.fixture
def presentation_domain() -> WordStudyDomain:
    """Provide Word study Presentation domain."""
    return WordStudyDomain()


@pytest.fixture
def service(
    mock_presentation_repo: Mock,
    mock_django_cache_storage: Mock,
    presentation_domain: WordStudyDomain,
) -> services.WordPresentationService:
    """Provide Presentation service."""
    return services.WordPresentationService(
        word_repo=mock_presentation_repo,
        case_storage=mock_django_cache_storage,
        domain=presentation_domain,
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
        mock_user: Mock,
        service: services.WordPresentationService,
        params: Mock,
        expected_case: Case,
    ) -> None:
        """Test get Presentation case."""
        # Act
        case = service.get_presentation_case(
            user=mock_user,
            presentation_params=params,
        )

        # Assert
        assert case == expected_case
