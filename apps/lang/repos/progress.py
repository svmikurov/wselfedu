"""Abstract base class for Update word study repository."""

import logging
from typing import override

from django.db import transaction
from django.db.utils import IntegrityError

from apps.lang import models, types
from apps.users.models import CustomUser

from .abc import ProgressABC

log = logging.getLogger(__name__)


class ProgressRepo(ProgressABC):
    """Word study Progress repository."""

    @override
    @transaction.atomic
    def update(
        self,
        user: CustomUser,
        translation_id: int,
        language: types.LanguageType,
        progress_delta: int,
    ) -> ProgressABC.UpdateResult:
        """Update Word study Progress."""
        model = models.TRANSLATION_MODELS[language]

        try:
            obj, created = model.objects.select_for_update().get_or_create(  # type: ignore[attr-defined]
                user=user,
                translation_id=translation_id,
                defaults={
                    'progress': max(0, min(progress_delta, model.MAX_PROGRESS))  # type: ignore[attr-defined]
                },
            )

            if not created:
                progress = obj.progress + progress_delta
                obj.progress = max(0, min(progress, model.MAX_PROGRESS))  # type: ignore[attr-defined]
                obj.save()

        except IntegrityError:
            log.error(
                'Database integrity error',
                extra={'translation_id': translation_id},
                exc_info=True,
            )

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise

        return {
            'created': created,
            'current_progress': obj.progress,
        }
