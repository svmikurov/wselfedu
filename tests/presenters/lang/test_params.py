"""Test Word study params presenter."""

from unittest.mock import Mock

import pytest

from apps.lang.repositories.abc import WordStudyParamsRepositoryABC
from apps.lang.types import WordParamsType
from apps.users.models import CustomUser
from di import container


@pytest.fixture
def initial_params() -> WordParamsType:
    """Get Word study params fixture."""
    return {
        'categories': [
            {'id': 2, 'name': 'category name'},
        ],
        'labels': [
            {'id': 3, 'name': 'label name'},
        ],
        'default': {
            'category': None,
            'label': {'id': 4, 'name': 'test label'},
            'word_count': 5,
        },
    }


@pytest.mark.django_db
class TestWordStudyParamsPresenter:
    """Test Word study params presenter."""

    @pytest.fixture
    def mock_repo(self, initial_params: WordParamsType) -> Mock:
        """Mock Word study params repository."""
        mock = Mock(spec=WordStudyParamsRepositoryABC)
        mock.fetch_initial.return_value = initial_params
        return mock

    def test_get_initial(
        self,
        user: CustomUser,
        initial_params: WordParamsType,
        mock_repo: Mock,
    ) -> None:
        """Get Word study initial params."""
        with container.lang.params_repo.override(mock_repo):
            presenter = container.lang.params_presenter()
            params = presenter.get_initial(user)

        assert params == initial_params
        mock_repo.fetch_initial.assert_called_once_with(user)
