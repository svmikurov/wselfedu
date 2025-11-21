"""Word study Presentation parameters Repository tests."""

from typing import Any

import pytest
from django.test.utils import CaptureQueriesContext

from apps.lang import models, repos
from apps.users.models import CustomUser

# Data fixtures
# ~~~~~~~~~~~~~


@pytest.fixture
def empty_parameters() -> dict[str, Any]:
    """Provide empty parameters DB data."""
    return {
        'categories': [],
        'marks': [],
        'category': None,
        'mark': None,
    }


@pytest.fixture
def parameters(
    user: CustomUser,
) -> dict[str, Any]:
    """Populate DB and provide parameters fixture."""
    category1 = models.LangCategory.objects.create(user=user, name='cat 1')
    mark1 = models.LangMark.objects.create(user=user, name='mark 1')
    mark2 = models.LangMark.objects.create(user=user, name='mark 2')
    models.Params.objects.create(
        user=user,
        # Set initial choices
        category=category1,
        mark=mark1,
    )
    return {
        'categories': [{'id': category1.id, 'name': 'cat 1'}],
        'marks': [
            {'id': mark1.id, 'name': 'mark 1'},
            {'id': mark2.id, 'name': 'mark 2'},
        ],
        'category': {'id': category1.id, 'name': 'cat 1'},
        'mark': {'id': mark1.id, 'name': 'mark 1'},
    }


# Instants fixtures
# ~~~~~~~~~~~~~~~~~


@pytest.fixture
def repo() -> repos.WordStudyParamsRepository:
    """Provide Word study Presentation params repository."""
    return repos.WordStudyParamsRepository()


# Tests
# ~~~~~


@pytest.mark.django_db
class TestFetch:
    """Fetch Word study Presentation params repository tests."""

    def test_fetch_empty_data(
        self,
        user: CustomUser,
        repo: repos.WordStudyParamsRepository,
        empty_parameters: dict[str, Any],
    ) -> None:
        """Test fetch initial empty data."""
        # Act & assert
        assert empty_parameters == repo.fetch(user)

    def test_fetch_data(
        self,
        user: CustomUser,
        repo: repos.WordStudyParamsRepository,
        parameters: dict[str, Any],
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test fetch initial data."""
        # Act & assert
        with django_assert_num_queries(3):  # type: ignore[operator]
            assert parameters == repo.fetch(user)
