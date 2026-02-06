"""Abstract base class for Update word study repository."""

import logging
from typing import override

from django.db import transaction
from django.db.models import Manager
from django.db.utils import IntegrityError

from apps.lang import models
from apps.study import models as study_models
from apps.users.models import Person

from ..models.abstract import AbstractProgressModel
from .abc import ProgressRepositoryABC

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
                models.EnglishTranslationProgress.objects
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


class ProgressRepository(ProgressRepositoryABC):
    """Item study progress repository."""

    def __init__(self, manager: Manager[AbstractProgressModel]) -> None:
        """Construct the repository."""
        self._manager = manager

    @override
    @transaction.atomic
    def update(self, user: Person, pk: int, delta: int) -> None:
        """Update item study progress."""
        max_progress = self._get_max_progress(user)

        try:
            obj = self.manager.get(pk=pk)
            new_progress = obj.progress + delta
            obj.progress = max(0, min(new_progress, max_progress))
            obj.save()

        except IntegrityError:
            log.error(
                'Database integrity error',
                extra={
                    'model': self.manager.model.__name__,
                    'pk': pk,
                },
                exc_info=True,
            )

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise

    @property
    @override
    def manager(self) -> Manager[AbstractProgressModel]:
        """Get model manager."""
        return self._manager

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
