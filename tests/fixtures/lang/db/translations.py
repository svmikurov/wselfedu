"""Translation query DB fixtures."""

from typing import Sequence

import pytest

from apps.core import models as models_core
from apps.lang import models, types
from apps.users.models import Person
from tests.fixtures.lang.no_db import translation as fixtures


@pytest.fixture
def translations(
    user: Person,
) -> list[models.EnglishTranslation]:
    """Populate DB with translations."""
    # Create native word model objects
    native_objs = [
        models.NativeWord(user=user, word=native)
        for native, _ in fixtures.TRANSLATIONS
    ]
    # Create english word model objects
    english_objs = [
        models.EnglishWord(user=user, word=english)
        for _, english in fixtures.TRANSLATIONS
    ]
    # Populate DB with native and english words
    models.NativeWord.objects.bulk_create(native_objs)
    models.EnglishWord.objects.bulk_create(english_objs)

    # Create native-english translation model objects
    translations_objs = [
        models.EnglishTranslation(user=user, native=nat, english=eng)
        for nat, eng in zip(native_objs, english_objs, strict=True)
    ]
    # Populate native-english translation model objects
    models.EnglishTranslation.objects.bulk_create(translations_objs)

    # Return native-english translation model object list
    return translations_objs


@pytest.fixture
def translations_meta(
    user: Person,
) -> tuple[
    list[models.LangCategory],
    list[models_core.Source],
    list[models.LangMark],
    list[models_core.Period],
]:
    """Populate DB with translations meta."""
    # Create translation category model objects
    category_objs = [
        models.LangCategory(user=user, name=name)
        for name in fixtures.CATEGORIES
    ]
    # Create translation source model objects
    source_objs = [
        models_core.Source(user=user, name=name) for name in fixtures.SOURCES
    ]
    # Create translation mark model objects
    marks_objs = [
        models.LangMark(user=user, name=name) for name in fixtures.MARKS
    ]

    period_objs = [
        models_core.Period(name=period['name']) for period in fixtures.PERIODS
    ]

    # Populate DB with translation meta data objects
    models.LangCategory.objects.bulk_create(category_objs)
    models_core.Source.objects.bulk_create(source_objs)
    models.LangMark.objects.bulk_create(marks_objs)
    models_core.Period.objects.bulk_create(period_objs)

    # Return translation meta data objects
    return category_objs, source_objs, marks_objs, period_objs


@pytest.fixture
def translation_settings(user: Person) -> models.TranslationSetting:
    """Provide translation settings model object."""
    return models.TranslationSetting.objects.create(
        user=user,
        word_count=fixtures.TRANSLATION_SETTINGS['word_count'],
    )


@pytest.fixture
def presentation_settings(user: Person) -> models.PresentationSettings:
    """Provide presentation settings model object."""
    return models.PresentationSettings.objects.create(
        user=user,
        question_timeout=fixtures.PRESENTATION_SETTINGS['question_timeout'],
        answer_timeout=fixtures.PRESENTATION_SETTINGS['answer_timeout'],
    )


@pytest.fixture
def parameters_db_data(
    user: Person,
    translations_meta: tuple[
        list[models.LangCategory],
        list[models_core.Source],
        list[models.LangMark],
        list[models_core.Period],
    ],
    translation_settings: models.TranslationSetting,
    presentation_settings: models.PresentationSettings,
) -> types.SetStudyParameters:
    """Provide Word study parameters."""
    categories, sources, marks, periods = translations_meta

    # Translation study presentation exercise parameters
    parameters = models.Parameters.objects.create(
        user=user,
        # Translation meta
        category=categories[0],
        mark=marks[1],
        word_source=sources[0],
        start_period=periods[0],
        end_period=periods[1],
        # progress field uses by default
        is_study=False,
        is_repeat=False,
        is_examine=True,
        is_know=False,
    )

    # TODO: Fix type ignore
    return {
        # Parameter options
        'categories': _build_choices(categories),
        'marks': _build_choices(marks),
        'sources': _build_choices(sources),
        'periods': _build_choices(periods),
        'translation_orders': fixtures.TRANSLATION_ORDERS,
        # Translation meta
        'category': {'id': categories[0].pk, 'name': categories[0].name},
        'mark': {'id': marks[1].pk, 'name': marks[1].name},
        'word_source': {'id': sources[0].pk, 'name': sources[0].name},
        'start_period': {'id': periods[0].pk, 'name': periods[0].name},
        'end_period': {'id': periods[1].pk, 'name': periods[1].name},
        # TODO: Add 'progress' field
        'is_study': parameters.is_study,  # type: ignore[typeddict-item]
        'is_repeat': parameters.is_repeat,  # type: ignore[typeddict-item]
        'is_examine': parameters.is_examine,  # type: ignore[typeddict-item]
        'is_know': parameters.is_know,  # type: ignore[typeddict-item]
        # Translation settings
        'translation_order': {  # type: ignore[typeddict-item]
            'code': translation_settings.translation_order.value,  # type: ignore[union-attr]
            'name': translation_settings.get_translation_order_display(),
        },
        'word_count': translation_settings.word_count,
        # Presentation settings
        'question_timeout': presentation_settings.question_timeout,
        'answer_timeout': presentation_settings.answer_timeout,
    }


def _build_choices(data: Sequence[types.HasIdName]) -> list[types.IdName]:
    """Build list of id-name dictionaries from model objects."""
    return [{'id': obj.id, 'name': obj.name} for obj in data]
