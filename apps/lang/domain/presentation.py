"""The domain logic to choice the translation for presentation case."""

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING, Literal

from apps.core import exceptions

from ..schemas import dto

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from .. import models, schemas

    # Translation data
    type Translations = QuerySet[models.EnglishTranslation]
    type Translation = models.EnglishTranslation

    # Presentation parameters & settings
    type Settings = schemas.SettingsModel
    type Order = Literal['to_native', 'to_foreign', 'random']
    type Ordered = Literal['to_native', 'to_foreign']

    # Presentation case
    type DomainResult = tuple[Case, CaseMeta]
    type Case = dto.TranslationCase
    type CaseMeta = dto.CaseMeta


class PresentationDomain:
    """Get presentation case."""

    @classmethod
    def get_case(
        cls, translations: Translations, settings: Settings
    ) -> DomainResult:
        """Get presentation case."""
        if not translations:
            raise exceptions.NoTranslationsAvailableException

        translation_limit = cls._get_limit(translations, settings.word_count)
        translation = cls._get_random(translation_limit)
        translation_order = cls._get_order(settings.translation_order)
        translation_case = cls._build_case(translation, translation_order)
        translation_meta = cls._build_meta(translation)
        return translation_case, translation_meta

    @staticmethod
    def _get_limit(
        translations: Translations, limit: int | None
    ) -> Translations:
        if limit is None:
            return translations
        # Temporary returns first translations
        # TODO: Implement translation limit order
        # after additional processing by service
        return translations.order_by('id')[:limit]

    @staticmethod
    def _get_random(translations: Translations) -> Translation:
        """Get random translation."""
        translation = choice(translations)
        return translation

    @staticmethod
    def _get_order(order: Order) -> Ordered:
        """Build translation order."""
        if order == 'random':
            return choice(['to_native', 'to_foreign'])
        return order

    @staticmethod
    def _build_case(translation: Translation, order: Ordered) -> Case:
        """Build presentation case DTO to render."""
        current_order = order or 'to_native'
        orders = {
            'to_native': {
                'question': translation.foreign,
                'answer': translation.native,
            },
            'to_foreign': {
                'question': translation.native,
                'answer': translation.foreign,
            },
        }
        return dto.TranslationCase(
            question=orders[current_order]['question'].word,
            answer=orders[current_order]['answer'].word,
            progress=str(translation.progress),
        )

    @staticmethod
    def _build_meta(translation: Translation) -> CaseMeta:
        """Build presentation case meta DTO to internal story."""
        return dto.CaseMeta(id=translation.pk)
