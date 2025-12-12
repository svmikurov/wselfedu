"""Web e2e translation test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.lang import models

if TYPE_CHECKING:
    from apps.users.models import Person


@pytest.fixture
def translation(
    user: Person,
) -> models.EnglishTranslation:
    """Provide english translation model instance."""
    return models.EnglishTranslation.objects.create(
        user=user,
        native=models.NativeWord.objects.create(user=user, word='привет'),
        english=models.EnglishWord.objects.create(user=user, word='hello'),
    )
