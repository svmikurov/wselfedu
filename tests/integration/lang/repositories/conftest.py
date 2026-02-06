"""Language discipline repository fixtures."""

import pytest

from apps.core import models as models_core
from apps.lang import repositories, types
from apps.lang.models import EnglishTranslation
from tests.fixtures.lang.no_db.translations import (
    EMPTY_TRANSLATION_PARAMETERS,
    PRESENTATION,
    PRESENTATION_CASE,
    TRANSLATION_ORDERS,
)

# Presentation data
# ~~~~~~~~~~~~~~~~~


@pytest.fixture
def presentation() -> types.PresentationDataT:
    """Provide presentation data."""
    return PRESENTATION


@pytest.fixture
def presentation_case() -> types.TranslationCase:
    """Provide Word study presentation case."""
    return PRESENTATION_CASE


@pytest.fixture
def conditions() -> types.CaseParametersAPI:
    """Provide Word study lookup empty conditions."""
    return EMPTY_TRANSLATION_PARAMETERS.copy()


# Presentation DB data
# ~~~~~~~~~~~~~~~~~~~~


@pytest.fixture
def public_parameters() -> types.CaseSettingsAPI:
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
        'display_orders': TRANSLATION_ORDERS,
        # Selected parameter
        'category': None,
        'mark': [],
        'word_source': None,
        'start_period': None,
        'end_period': None,
        'display_order': TRANSLATION_ORDERS[1],
        'is_study': True,
        'is_repeat': True,
        'is_examine': True,
        'is_know': False,
        # Set parameter
        'word_count': None,
        'question_timeout': 3,
        'answer_timeout': 3,
    }


# Repositories
# ~~~~~~~~~~~~


@pytest.fixture
def parameters_repo() -> repositories.StudyParametersRepository:
    """Provide Word study Presentation params repository."""
    return repositories.StudyParametersRepository()


@pytest.fixture
def repository() -> repositories.ProgressRepository:
    """Provide English translation progress repository."""
    return repositories.ProgressRepository(EnglishTranslation.objects)


@pytest.fixture
def assigned_progress_repository() -> (
    repositories.AssignedTranslationProgressRepository
):
    """Provide Assigned translation study progress repository."""
    return repositories.AssignedTranslationProgressRepository()
