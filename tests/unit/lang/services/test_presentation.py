"""Word study Presentation service tests."""

import uuid
from unittest.mock import Mock

import pytest

from apps.lang import services, types
from apps.lang.repos.abc import PresentationABC
from apps.lang.services.study import WordStudyDomain


@pytest.fixture
def mock_presentation_repo(
    presentation: types.PresentationT,
) -> Mock:
    """Mock Word study Presentation repository."""
    mock = Mock(spec=PresentationABC)
    mock.get_candidates.return_value = types.WordStudyParams(
        translation_ids=[1],
    )
    mock.get_case.return_value = presentation
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
    presentation: types.PresentationDataT,
) -> types.PresentationCaseT:
    """Provide Word study Presentation case."""
    case: types.PresentationCaseT = {'case_uuid': case_uuid, **presentation}
    return case


@pytest.fixture
def params() -> Mock:
    """Provide Word study Presentation params."""
    return Mock(spec=types.ParamsChoicesT)


class TestService:
    """Test Presentation service."""

    def test_get_presentation_case(
        self,
        mock_user: Mock,
        service: services.WordPresentationService,
        params: Mock,
        expected_case: types.PresentationCaseT,
    ) -> None:
        """Test get Presentation case."""
        # Act
        case = service.get_presentation_case(
            user=mock_user,
            presentation_params=params,
        )

        # Assert
        assert case == expected_case
