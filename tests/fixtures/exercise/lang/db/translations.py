"""Translations DB fixtures."""

import pytest
from django.db.models import F

from apps.lang import models
from apps.users.models import Person
from ports.interfaces.schemas.domain.exercise.exercise import TaskItem

from ..no_db.translations import TRANSLATIONS


@pytest.fixture
def translations(
    user: Person,
) -> list[TaskItem]:
    """Populate DB with translations."""
    # Create native word model objects
    native_objs = [
        models.NativeWord(user=user, word=native) for native, _ in TRANSLATIONS
    ]
    # Create english word model objects
    english_objs = [
        models.EnglishWord(user=user, word=english)
        for _, english in TRANSLATIONS
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

    queryset = (
        models.EnglishTranslation.objects.filter(
            user=user,
        )
        .select_related('native', 'foreign')
        .annotate(
            define=F('native__word'),
            mean=F('foreign__word'),
            progress_value=F('progress'),
        )
    ).order_by('id')
    candidates = [TaskItem.model_validate(candidate) for candidate in queryset]
    # Return native-english translation model object list
    return candidates
