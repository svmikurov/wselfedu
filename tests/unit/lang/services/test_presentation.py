"""Word study Presentation service tests."""

from unittest.mock import Mock

import pytest

from apps.lang import domain, repositories, services, types
from tests.fixtures.lang.no_db import translations as fixtures


@pytest.fixture
def mock_presentation_repo() -> Mock:
    """Mock Word study Presentation repository."""
    mock = Mock(spec=repositories.PresentationABC)
    mock.get_candidates.return_value = types.WordStudyParameters(
        translation_ids=[1],
    )
    mock.get_translation.return_value = fixtures.PRESENTATION
    return mock


@pytest.fixture
def presentation_domain() -> domain.WordStudyDomain:
    """Provide Word study Presentation domain."""
    return domain.WordStudyDomain()


@pytest.fixture
def service(
    mock_presentation_repo: Mock,
    mock_task_storage: Mock,
    presentation_domain: domain.WordStudyDomain,
) -> services.WordPresentationService:
    """Provide Presentation service."""
    return services.WordPresentationService(
        word_repo=mock_presentation_repo,
        case_storage=mock_task_storage,
        domain=presentation_domain,
    )


@pytest.fixture
def expected_case() -> types.TranslationCase:
    """Provide Word study Presentation case."""
    return {
        'case_uuid': fixtures.TRANSLATION_CASE_UUID,
        **fixtures.PRESENTATION,
    }


@pytest.fixture
def parameters() -> Mock:
    """Provide Word study Presentation params."""
    return Mock(spec=types.Options)


class TestService:
    """Test Presentation service."""

    def test_get_presentation_case(
        self,
        mock_user: Mock,
        service: services.WordPresentationService,
        parameters: Mock,
        expected_case: types.TranslationCase,
    ) -> None:
        """Test get Presentation case."""
        # Act
        case = service.get_case(
            user=mock_user,
            presentation_params=parameters,
        )

        # Assert
        assert case == expected_case
