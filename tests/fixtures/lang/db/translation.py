"""English translation fixtures."""

import pytest

from apps.lang import models
from apps.users.models import Person

from ..no_db import translations as fixtures


@pytest.fixture
def native_word(user: Person) -> models.NativeWord:
    """Native word."""
    return models.NativeWord.objects.create(
        user=user,
        word=fixtures.PRESENTATION['explanation'],
    )


@pytest.fixture
def english_word(user: Person) -> models.EnglishWord:
    """English word."""
    return models.EnglishWord.objects.create(
        user=user,
        word=fixtures.PRESENTATION['definition'],
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
        english=english_word,
    )


@pytest.fixture
def english_progress(
    user: Person,
    word_translation: models.EnglishTranslation,
) -> models.EnglishProgress:
    """Get english word translation."""
    return models.EnglishProgress.objects.create(  # type: ignore[misc]
        user=user,
        translation=word_translation,
        progress=fixtures.PRESENTATION['info']['progress'],
    )
