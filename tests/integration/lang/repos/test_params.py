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
def public_parameters(
    translation_order_options: list[types.CodeName],
) -> dict[
    str,
    list[types.IdName] | list[types.CodeName] | types.TranslateOrderT | None,
]:
    """Provide public DB data."""
    # Create public parameter choices
    periods = core_models.Period.objects.bulk_create(
        [
            core_models.Period(name='start'),
            core_models.Period(name='end'),
        ]
    )

    # TODO: Fix type ignore
    # Add protocol of typed dict instead Literal?
    return {
        # Parameter options
        'categories': [],
        'marks': [],
        'sources': [],
        # - public options
        'periods': [  # type: ignore[dict-item]
            {'id': periods[0].pk, 'name': periods[0].name},
            {'id': periods[1].pk, 'name': periods[1].name},
        ],
        'orders': translation_order_options,
        # Selected parameter
        'category': None,
        'mark': None,
        'word_source': None,
        'start_period': None,
        'end_period': None,
        'order': translation_order_options[1],  # type: ignore[dict-item]
        # Set parameter
        'word_count': None,
        'question_timeout': None,
        'answer_timeout': None,
    }


# TODO: Update return type to `apps.lang.types.WordPresentationParamsT`
# after completion of the repo implementation
@pytest.fixture
def parameters(
    user: CustomUser,
    translation_order_options: list[types.CodeName],
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
    periods = core_models.Period.objects.bulk_create(
        [
            core_models.Period(name='start'),
            core_models.Period(name='end'),
        ]
    )

    # Set initial choices
    parameters = models.Params.objects.create(
        user=user,
        category=category1,
        mark=marks[0],
        word_source=source1,
        word_count=67,
        start_period=periods[0],
        end_period=periods[1],
        question_timeout=2.1,
        answer_timeout=1.2,
    )

    # TODO: Fix type ignore
    # Expected parameters data
    return {
        # Parameter options
        'categories': [{'id': category1.pk, 'name': 'cat 1'}],
        'marks': [
            {'id': marks[0].pk, 'name': 'mark 1'},
            {'id': marks[1].pk, 'name': 'mark 2'},
        ],
        'sources': [{'id': source1.pk, 'name': 'source 1'}],
        'periods': [
            {'id': periods[0].pk, 'name': 'start'},
            {'id': periods[1].pk, 'name': 'end'},
        ],
        'orders': translation_order_options,
        # Selected parameter
        'category': {'id': category1.pk, 'name': 'cat 1'},
        'mark': {'id': marks[0].pk, 'name': 'mark 1'},
        'word_source': {'id': source1.pk, 'name': source1.name},
        'start_period': {'id': periods[0].pk, 'name': periods[0].name},
        'end_period': {'id': periods[1].pk, 'name': periods[1].name},
        'order': {
            'code': parameters.order.value,  # type: ignore[union-attr]
            'name': parameters.order.label,  # type: ignore[union-attr]
        },
        # Set parameter
        'word_count': parameters.word_count,
        'question_timeout': parameters.question_timeout,
        'answer_timeout': parameters.answer_timeout,
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

    def test_fetch_public_parameters(
        self,
        user: CustomUser,
        repo: repos.WordStudyParamsRepository,
        public_parameters: dict[str, Any],
    ) -> None:
        """Test fetch public default data."""
        # Act & assert
        assert public_parameters == repo.fetch(user)

    def test_fetch_data(
        self,
        user: CustomUser,
        repo: repos.WordStudyParamsRepository,
        parameters: dict[str, Any],
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test fetch initial data."""
        # Act & assert
        with django_assert_num_queries(5):  # type: ignore[operator]
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
            key: parameters[key]
            for key in parameters.keys()
            if key not in ('categories', 'marks', 'sources', 'periods')
        }
        new_params['mark'] = mark
        new_params['word_count'] = 76

        # - Expected new parameter data
        expected = parameters.copy()
        expected['mark'] = mark
        expected['word_count'] = 76

        # Act
        with django_assert_num_queries(8):  # type: ignore[operator]
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
                'start_period',
                'end_period',
                'question_timeout',
                'answer_timeout',
            )
        }
        expected = {**parameters, **update_data}

        # Act & Assert
        assert expected == repo.update(user, update_data)  # type: ignore[arg-type]
