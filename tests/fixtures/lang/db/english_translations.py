"""Translation query DB fixtures."""

import pytest

from apps.core import models as models_core
from apps.lang import models
from apps.users.models import CustomUser

from ..no_db import translation_query as data


@pytest.fixture
def translations(
    user: CustomUser,
) -> list[models.EnglishTranslation]:
    """Populate DB with translations."""
    # Create native word model objects
    native_objs = [
        models.NativeWord(user=user, word=native)
        for native, _ in data.TRANSLATIONS
    ]
    # Create english word model objects
    english_objs = [
        models.EnglishWord(user=user, word=english)
        for _, english in data.TRANSLATIONS
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
    user: CustomUser,
) -> tuple[
    list[models.LangCategory],
    list[models_core.Source],
    list[models.LangMark],
]:
    """Populate DB with translations meta."""
    # Create translation category model objects
    category_objs = [
        models.LangCategory(user=user, name=name) for name in data.CATEGORIES
    ]
    # Create translation source model objects
    source_objs = [
        models_core.Source(user=user, name=name) for name in data.SOURCES
    ]
    # Create translation mark model objects
    marks_objs = [models.LangMark(user=user, name=name) for name in data.MARKS]

    # Populate DB with translation meta data objects
    models.LangCategory.objects.bulk_create(category_objs)
    models_core.Source.objects.bulk_create(source_objs)
    models.LangMark.objects.bulk_create(marks_objs)

    # Return translation meta data objects
    return category_objs, source_objs, marks_objs
