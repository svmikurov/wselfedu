"""Translation presenters."""

from typing import NamedTuple

from django.db.models.query import QuerySet

from apps.users.models import CustomUser

from .. import models


class TranslationParams(NamedTuple):
    """Get translation params."""

    user: CustomUser
    labels: list[models.LangLabel] | None


class Translations(NamedTuple):
    """English word translations."""

    pk: int
    native: models.NativeWord
    english: models.EnglishWord


class EnglishTranslationPresenter:
    """English word translation presenter."""

    def get_translations(
        self,
        params: TranslationParams | None = None,
    ) -> QuerySet[models.EnglishTranslation]:
        """Get English word translations."""
        return models.EnglishTranslation.objects.all()
