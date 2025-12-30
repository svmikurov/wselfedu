"""Abstract base class for Update word study repository."""

import logging
from typing import override

from django.db import transaction
from django.db.utils import IntegrityError

from apps.lang import models
from apps.study import models as study_models
from apps.users.models import Person

from .abc import ProgressABC

log = logging.getLogger(__name__)


class Progress(ProgressABC):
    """Word study Progress repository."""

    @override
    @transaction.atomic
    def update(
        self,
        user: Person,
        translation_id: int,
        progress_delta: int,
    ) -> None:
        """Update Word study Progress."""
        max_progress = self._get_max_progress(user)

        try:
            obj = models.EnglishTranslation.objects.select_for_update().get(
                pk=translation_id
            )
            new_progress = obj.progress + progress_delta
            obj.progress = max(0, min(new_progress, max_progress))
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

    @staticmethod
    def _get_max_progress(user: Person) -> int:
        # Get parameters
        parameters = (
            models.Parameters.objects.filter(user=user)
            .select_related('progress')
            .first()
        )

        # Get 'know' progress value as max progress
        max_progress = (
            parameters.progress.know
            if parameters and parameters.progress
            else study_models.Progress.KNOW_DEFAULT
        )
        return max_progress
