"""Language discipline repository fixtures."""

import pytest

from apps.core import models as models_core
from apps.lang import models, repositories, types
from apps.users.models import Person
from tests.fixtures.lang.no_db.translation_parameters import (
    TRANSLATION_ORDERS,
)
from tests.fixtures.lang.no_db.translation_query import (
    EMPTY_LOOKUP_CONDITIONS,
    PRESENTATION,
    PRESENTATION_CASE,
)

# Presentation data
# ~~~~~~~~~~~~~~~~~


@pytest.fixture
def presentation() -> types.PresentationDataT:
    """Provide presentation data."""
    return PRESENTATION


@pytest.fixture
def presentation_case() -> types.PresentationCaseT:
    """Provide Word study presentation case."""
    return PRESENTATION_CASE


@pytest.fixture
def conditions() -> types.WordParameters:
    """Provide Word study lookup empty conditions."""
    return EMPTY_LOOKUP_CONDITIONS.copy()


# Presentation DB data
# ~~~~~~~~~~~~~~~~~~~~


@pytest.fixture
def public_parameters() -> types.SetStudyParameters:
    """Provide public DB data."""
    # Create public parameter choices
    periods = models_core.Period.objects.bulk_create(
        [
            models_core.Period(name='start'),
            models_core.Period(name='end'),
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
        'periods': [
            {'id': periods[0].pk, 'name': periods[0].name},
            {'id': periods[1].pk, 'name': periods[1].name},
        ],
        'translation_orders': TRANSLATION_ORDERS,
        # Selected parameter
        'category': None,
        'mark': None,
        'word_source': None,
        'start_period': None,
        'end_period': None,
        'translation_order': TRANSLATION_ORDERS[1],
        'is_study': True,
        'is_repeat': True,
        'is_examine': True,
        'is_know': False,
        # Set parameter
        'word_count': None,
        'question_timeout': None,
        'answer_timeout': None,
    }


# TODO: Update return type to `apps.lang.types.WordPresentationParamsT`
# after completion of the repo implementation
@pytest.fixture
def parameters(user: Person) -> types.SetStudyParameters:
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
    source1 = models_core.Source.objects.create(user=user, name='source 1')
    periods = models_core.Period.objects.bulk_create(
        [
            models_core.Period(name='start'),
            models_core.Period(name='end'),
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
        is_study=True,
        is_repeat=False,
        is_examine=False,
        is_know=False,
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
        'translation_orders': TRANSLATION_ORDERS,
        # Selected parameter
        'category': {'id': category1.pk, 'name': 'cat 1'},
        'mark': {'id': marks[0].pk, 'name': 'mark 1'},
        'word_source': {'id': source1.pk, 'name': source1.name},
        'start_period': {'id': periods[0].pk, 'name': periods[0].name},
        'end_period': {'id': periods[1].pk, 'name': periods[1].name},
        'translation_order': {  # type: ignore[typeddict-item]
            'code': parameters.translation_order.value,  # type: ignore[union-attr]
            'name': parameters.translation_order.label,  # type: ignore[union-attr]
        },
        'is_study': parameters.is_study,  # type: ignore[typeddict-item]
        'is_repeat': parameters.is_repeat,  # type: ignore[typeddict-item]
        'is_examine': parameters.is_examine,  # type: ignore[typeddict-item]
        'is_know': parameters.is_know,  # type: ignore[typeddict-item]
        # Set parameter
        'word_count': parameters.word_count,
        'question_timeout': parameters.question_timeout,
        'answer_timeout': parameters.answer_timeout,
    }


# Repositories
# ~~~~~~~~~~~~


@pytest.fixture
def parameters_repo() -> repositories.WordStudyParametersRepository:
    """Provide Word study Presentation params repository."""
    return repositories.WordStudyParametersRepository()


@pytest.fixture
def presentation_repo() -> repositories.EnglishPresentation:
    """Provide Word study Presentation repository."""
    return repositories.EnglishPresentation()


@pytest.fixture
def progress_repo() -> repositories.Progress:
    """Provide Word study Progress repository."""
    return repositories.Progress()
