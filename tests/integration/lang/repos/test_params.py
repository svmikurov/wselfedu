"""Word study Presentation parameters Repository tests."""

from typing import Any

import pytest
from django.test.utils import CaptureQueriesContext

from apps.core import models as core_models
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
        'sources': [],
        'category': None,
        'mark': None,
        'word_source': None,
    }


@pytest.fixture
def parameters(
    user: CustomUser,
) -> dict[str, Any]:
    """Populate DB and provide parameters."""
    # Create choices
    category1 = models.LangCategory.objects.create(user=user, name='cat 1')
    marks = models.LangMark.objects.bulk_create(
        [
            models.LangMark(user=user, name='mark 1'),
            models.LangMark(user=user, name='mark 2'),
        ],
        batch_size=None,
    )
    source1 = core_models.Source.objects.create(user=user, name='source 1')

    # Set initial choices
    models.Params.objects.create(
        user=user,
        category=category1,
        mark=marks[0],
        word_source=source1,
    )
    return {
        'categories': [{'id': category1.id, 'name': 'cat 1'}],
        'marks': [
            {'id': marks[0].id, 'name': 'mark 1'},
            {'id': marks[1].id, 'name': 'mark 2'},
        ],
        'category': {'id': category1.id, 'name': 'cat 1'},
        'sources': [{'id': source1.id, 'name': 'source 1'}],
        'mark': {'id': marks[0].id, 'name': 'mark 1'},
        'word_source': {'id': source1.id, 'name': source1.name},
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
        with django_assert_num_queries(4):  # type: ignore[operator]
            assert parameters == repo.fetch(user)
