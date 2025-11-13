"""Abstract base class for Update word study repository."""

from typing import ClassVar, Type, override

from django.db import transaction
from django.db.models import Model

from apps.lang import models, types

from .abc import UpdateWordProgressRepoABC


class UpdateWordProgressRepo(UpdateWordProgressRepoABC):
    """Update word study repository."""

    TRANSLATION_MODELS: ClassVar[dict[types.LanguageType, Type[Model]]] = {
        'english': models.EnglishProgress,
    }

    @override
    @transaction.atomic
    def update(
        self,
        translation_id: int,
        language: types.LanguageType,
        progress_case: types.ProgressType,
        progress_value: int,
    ) -> None:
        """Update word study progress."""
        match progress_case:
            case 'known':
                progress_delta = progress_value
            case 'unknown':
                progress_delta = -progress_value

        try:
            model = self.TRANSLATION_MODELS[language]

            translation = models.EnglishTranslation.objects.get(
                pk=translation_id
            )

            model.objects.select_for_update().update_or_create(  # type: ignore[attr-defined]
                user=translation.user,
                translation_id=translation_id,
                progress=progress_delta,
            )

        except models.EnglishProgress.DoesNotExist:
            ...
