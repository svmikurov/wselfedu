"""Word study parameters API test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import pytest

from apps.core import models as models_core
from apps.lang import models, types
from tests.fixtures.lang.no_db import word_study_params as fixtures

if TYPE_CHECKING:
    from apps.users.models import Person


@pytest.fixture
def translation_order_options() -> list[types.CodeName]:
    """Provide translation order options."""
    return fixtures.TRANSLATION_ORDERS


@pytest.fixture
def public_parameters(
    parameters_db_data: types.SetStudyParameters,
    translation_order_options: list[types.CodeName],
) -> types.SetStudyParameters:
    """Provide public Parameters data.

    Contains fields for a user who has no saved settings
    or the field is not set in the user settings.
    """
    return {
        # Parameter options
        'categories': [],
        'marks': [],
        'sources': [],
        'periods': parameters_db_data['periods'],
        'translation_orders': translation_order_options,
        # Selected parameter
        'category': None,
        'mark': None,
        'word_source': None,
        'start_period': None,
        'end_period': None,
        'translation_order': translation_order_options[1],
        # Set parameter
        'word_count': None,
        'question_timeout': None,
        'answer_timeout': None,
    }


@pytest.fixture
def parameters_db_data(
    user: Person,
    translation_order_options: list[types.CodeName],
) -> types.SetStudyParameters:
    """Provide Word study Presenter DB data parameters."""
    categories = models.LangCategory.objects.bulk_create(
        [
            models.LangCategory(user=user, name='cat 1'),
            models.LangCategory(user=user, name='cat 2'),
        ],
        batch_size=None,
    )
    marks = models.LangMark.objects.bulk_create(
        [
            models.LangMark(user=user, name='mark 1'),
            models.LangMark(user=user, name='mark 2'),
        ],
        batch_size=None,
    )
    sources = models_core.Source.objects.bulk_create(
        [
            models_core.Source(user=user, name='source 1'),
            models_core.Source(user=user, name='source 2'),
        ],
        batch_size=None,
    )
    periods = models_core.Period.objects.bulk_create(
        [
            models_core.Period(name='start'),
            models_core.Period(name='end'),
        ]
    )

    parameters = models.Params.objects.create(
        user=user,
        # Initial choices
        category=categories[0],
        mark=marks[1],
        word_source=sources[0],
        word_count=80,
        start_period=periods[0],
        end_period=periods[1],
        question_timeout=2.9,
        answer_timeout=3.1,
    )

    # TODO: Fix type ignore
    return {
        # Parameter options
        'categories': _build_choices(categories),
        'marks': _build_choices(marks),
        'sources': _build_choices(sources),
        'periods': _build_choices(periods),
        'translation_orders': translation_order_options,
        # Selected parameter
        'category': {'id': categories[0].pk, 'name': categories[0].name},
        'mark': {'id': marks[1].pk, 'name': marks[1].name},
        'word_source': {'id': sources[0].pk, 'name': sources[0].name},
        'start_period': {'id': periods[0].pk, 'name': periods[0].name},
        'end_period': {'id': periods[1].pk, 'name': periods[1].name},
        'translation_order': {  # type: ignore[typeddict-item]
            'code': parameters.translation_order.value,  # type: ignore[union-attr]
            'name': parameters.translation_order.label,  # type: ignore[union-attr]
        },
        # Set parameter
        'word_count': parameters.word_count,
        'question_timeout': parameters.question_timeout,
        'answer_timeout': parameters.answer_timeout,
    }


def _build_choices(data: Sequence[types.HasIdName]) -> list[types.IdName]:
    """Build list of id-name dictionaries from model objects."""
    return [{'id': d.id, 'name': d.name} for d in data]
