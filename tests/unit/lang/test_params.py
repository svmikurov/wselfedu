"""Test Word study params presenter."""

from unittest.mock import Mock

import pytest

from apps.lang import types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser
from di import container


@pytest.fixture
def initial_params() -> types.WordPresentationParamsT:
    """Get Word study params fixture."""
    return {
        'categories': [{'id': 2, 'name': 'category name'}],
        'labels': [{'id': 3, 'name': 'label name'}],
        'category': None,
        'label': None,
        # TODO: Add database tables for choices
        'word_source': None,
        'order': None,
        'start_period': None,
        'end_period': None,
        'word_count': None,
        'question_timeout': None,
        'answer_timeout': None,
    }


@pytest.mark.django_db
class TestWordStudyParamsPresenter:
    """Test Word study params presenter."""

    @pytest.fixture
    def mock_repo(self, initial_params: types.ParamsChoicesT) -> Mock:
        """Mock Word study params repository."""
        mock = Mock(spec=WordStudyParamsRepositoryABC)
        mock.fetch_initial.return_value = initial_params
        return mock

    def test_get_initial(
        self,
        user: CustomUser,
        initial_params: types.ParamsChoicesT,
        mock_repo: Mock,
    ) -> None:
        """Get Word study initial params."""
        with container.lang.params_repo.override(mock_repo):
            repository = container.lang.params_repo()
            params = repository.fetch_initial(user)

        assert params == initial_params
        mock_repo.fetch_initial.assert_called_once_with(user)
