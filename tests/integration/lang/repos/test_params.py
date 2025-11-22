"""Word study Presentation parameters Repository tests."""

from typing import Any

import pytest
from django.test.utils import CaptureQueriesContext

from apps.core import models as core_models
from apps.lang import models, repos, types
from apps.users.models import CustomUser

pytestmark = pytest.mark.django_db

# Data fixtures
# ~~~~~~~~~~~~~


@pytest.fixture
def empty_parameters() -> dict[str, list[types.IdName] | None]:
    """Provide empty parameters DB data."""
    return {
        'categories': [],
        'marks': [],
        'sources': [],
        'category': None,
        'mark': None,
        'word_source': None,
        'word_count': None,
    }


# TODO: Update return type to `apps.lang.types.WordPresentationParamsT`
# after completion of the repo implementation
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
    parameters = models.Params.objects.create(
        user=user,
        category=category1,
        mark=marks[0],
        word_source=source1,
        word_count=67,
    )

    # Parameters data
    return {
        'categories': [{'id': category1.id, 'name': 'cat 1'}],
        'marks': [
            {'id': marks[0].id, 'name': 'mark 1'},
            {'id': marks[1].id, 'name': 'mark 2'},
        ],
        'sources': [{'id': source1.id, 'name': 'source 1'}],
        'category': {'id': category1.id, 'name': 'cat 1'},
        'mark': {'id': marks[0].id, 'name': 'mark 1'},
        'word_source': {'id': source1.id, 'name': source1.name},
        'word_count': parameters.word_count,
    }


# Instants fixtures
# ~~~~~~~~~~~~~~~~~


@pytest.fixture
def repo() -> repos.WordStudyParamsRepository:
    """Provide Word study Presentation params repository."""
    return repos.WordStudyParamsRepository()


# Tests
# ~~~~~


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


class TestUpdate:
    """Update Word study Presentation params repository tests."""

    def test_update_parameters(
        self,
        user: CustomUser,
        repo: repos.WordStudyParamsRepository,
        parameters: dict[str, Any],
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test update initial data."""
        # Arrange
        # - Select a parameter from the options
        # to set it as the initial value
        mark = parameters['marks'][1]

        # - Parameter data without option fields to update
        new_params = {
            key: parameters[key] for key in ('category', 'mark', 'word_source')
        }
        new_params['mark'] = mark
        new_params['word_count'] = 76

        # - Expected new parameter data
        expected = parameters.copy()
        expected['mark'] = mark
        expected['word_count'] = 76

        # Act
        with django_assert_num_queries(7):  # type: ignore[operator]
            updated_parameters = repo.update(user, new_params)  # type: ignore[arg-type]

        # Assert
        assert expected == updated_parameters

    def test_update_with_none(
        self,
        user: CustomUser,
        repo: repos.WordStudyParamsRepository,
        parameters: dict[str, Any],
    ) -> None:
        """Test that updated parameter is None."""
        # Arrange
        update_data = {
            key: None
            for key in (
                'category',
                'mark',
                'word_source',
                'word_count',
            )
        }
        expected = {**parameters, **update_data}

        # Act & Assert
        assert expected == repo.update(user, update_data)  # type: ignore[arg-type]
