"""Fixtures tests."""

import pytest

from apps.lang import models


@pytest.mark.django_db
def test_fixtures(
    translations: list[models.EnglishTranslation],
) -> None:
    """Test translation fixtures."""
    print(f'{translations = }')
