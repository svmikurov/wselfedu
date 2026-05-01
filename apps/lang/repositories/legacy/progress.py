"""Abstract base class for Update word study repository."""

import logging

from django.db import transaction
from django.db.utils import IntegrityError

from apps.lang import models

log = logging.getLogger(__name__)


class AssignedTranslationProgressRepository:
    """Assigned English translation study progress repository."""

    @transaction.atomic
    def update(
        self, user_pk: int, translation_pk: int, delta: int, max_progress: int
    ) -> None:
        """Update progress of study assigned English translation."""
        try:
            # fmt: off
            obj = (
                models.EnglishTranslationStudyProgress.objects
                .select_for_update()
                .get(user_id=user_pk, translation_id=translation_pk)
            )
            # fmt: on

            new_progress = obj.value + delta
            obj.value = max(0, min(new_progress, max_progress))
            obj.save()

        except IntegrityError:
            log.error(
                'Database integrity error',
                extra={'translation_pk': translation_pk},
                exc_info=True,
            )

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise
