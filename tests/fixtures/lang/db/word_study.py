"""Word study DB fixtures."""

import pytest

from apps.lang import models, types
from apps.users.models import Person


@pytest.fixture
def native_word(
    user: Person,
    presentation: types.PresentationT,
) -> models.NativeWord:
    """Native word fixture."""
    return models.NativeWord.objects.create(
        user=user,
        word=presentation['explanation'],
    )


@pytest.fixture
def english_word(
    user: Person,
    presentation: types.PresentationT,
) -> models.EnglishWord:
    """English word fixture."""
    return models.EnglishWord.objects.create(
        user=user,
        word=presentation['definition'],
    )


@pytest.fixture
def word_translation(
    user: Person,
    native_word: models.NativeWord,
    english_word: models.EnglishWord,
) -> models.EnglishTranslation:
    """Get word translation."""
    return models.EnglishTranslation.objects.create(
        user=user, native=native_word, english=english_word
    )


@pytest.fixture
def english_progress(
    user: Person,
    presentation: types.PresentationT,
    word_translation: models.EnglishTranslation,
) -> models.EnglishProgress:
    """Get translation fixture."""
    return models.EnglishProgress.objects.create(
        user=user,
        translation=word_translation,
        progress=presentation['info']['progress'],  # type: ignore[typeddict-item]
    )
