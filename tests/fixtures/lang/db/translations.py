"""Translation query DB fixtures."""

import pytest

from apps.core import models as models_core
from apps.lang import models
from apps.users.models import Person
from tests.fixtures.lang.no_db import translations as fixtures

# ---------------------------------------------------
# Populate DB with `PRESENTATION` translation fixture
# ---------------------------------------------------


@pytest.fixture
def native_word(user: Person) -> models.NativeWord:
    """Native word."""
    return models.NativeWord.objects.create(
        user=user,
        word=fixtures.PRESENTATION['answer'],
    )


@pytest.fixture
def english_word(user: Person) -> models.EnglishWord:
    """English word."""
    return models.EnglishWord.objects.create(
        user=user,
        word=fixtures.PRESENTATION['question'],
    )


@pytest.fixture
def word_translation(
    user: Person,
    native_word: models.NativeWord,
    english_word: models.EnglishWord,
) -> models.EnglishTranslation:
    """Get word translation."""
    return models.EnglishTranslation.objects.create(
        user=user,
        native=native_word,
        foreign=english_word,
    )


# ---------------------------------------
# Populate DB with `TRANSLATIONS` fixture
# ---------------------------------------


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
        models.EnglishTranslation(user=user, native=nat, foreign=eng)
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
    list[models.Category],
    list[models_core.Source],
    list[models.Mark],
    list[models_core.Period],
]:
    """Populate DB with translations meta."""
    # Create translation category model objects
    category_objs = [
        models.Category(user=user, name=name) for name in fixtures.CATEGORIES
    ]
    # Create translation source model objects
    source_objs = [
        models_core.Source(user=user, name=name) for name in fixtures.SOURCES
    ]
    # Create translation mark model objects
    marks_objs = [models.Mark(user=user, name=name) for name in fixtures.MARKS]

    period_objs = [
        models_core.Period(name=period['name']) for period in fixtures.PERIODS
    ]

    # Populate DB with translation meta data objects
    models.Category.objects.bulk_create(category_objs)
    models_core.Source.objects.bulk_create(source_objs)
    models.Mark.objects.bulk_create(marks_objs)
    models_core.Period.objects.bulk_create(period_objs)

    # Return translation meta data objects
    return category_objs, source_objs, marks_objs, period_objs
