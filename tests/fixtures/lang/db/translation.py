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
