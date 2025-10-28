"""Test Word study params presenter."""

from unittest.mock import Mock

import pytest

from apps.lang.orchestrators.abc import WordStudyParamsOrchestratorABC
from apps.lang.types import WordParamsType
from apps.users.models import CustomUser
from di import container


@pytest.fixture
def initial_params() -> WordParamsType:
    """Get Word study params fixture."""
    return {
        'user_id': 1,
        'categories': [
            {'id': 2, 'name': 'category name'},
        ],
        'labels': [
            {'id': 3, 'name': 'label name'},
        ],
    }


@pytest.mark.django_db
class TestWordStudyParamsPresenter:
    """Test Word study params presenter."""

    @pytest.fixture
    def orchestrator_mock(self, initial_params: WordParamsType) -> Mock:
        """Mock Word study params orchestrator."""
        mock = Mock(spec=WordStudyParamsOrchestratorABC)
        mock.fetch_initial.return_value = initial_params
        return mock

    def test_get_initial(
        self,
        user: CustomUser,
        initial_params: WordParamsType,
        orchestrator_mock: Mock,
    ) -> None:
        """Get Word study initial params."""
        with container.lang.params_orchestrator.override(orchestrator_mock):
            presenter = container.lang.params_presenter()
            params = presenter.get_initial(user)

        assert params == initial_params
        orchestrator_mock.fetch_initial.assert_called_once_with(user)
