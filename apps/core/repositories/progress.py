"""Exercise progress repository."""

import logging
from typing import override

from django.db import transaction
from django.db.models import Manager
from django.db.utils import IntegrityError

from apps.core.repositories.abstract import AbstractProgressRepository
from apps.lang import models
from apps.lang.models.abstract import AbstractProgressModel
from apps.study import models as study_models
from apps.users.models import Person

log = logging.getLogger(__name__)


class ProgressRepository(AbstractProgressRepository):
    """Item study progress repository."""

    def __init__(
        self,
        manager: Manager[AbstractProgressModel],
    ) -> None:
        """Construct the repository."""
        self._manager = manager

    @override
    @transaction.atomic
    def update(self, user: Person, pk: int, delta: int) -> None:
        """Update item study progress."""
        max_progress = self._get_max_progress(user)

        try:
            obj = self._manager.get(pk=pk)
            new_progress = obj.progress + delta
            obj.progress = max(0, min(new_progress, max_progress))
            obj.save()

        except IntegrityError:
            log.error(
                'Database integrity error',
                extra={
                    'model': self._manager.model.__name__,
                    'pk': pk,
                },
                exc_info=True,
            )

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise

    @staticmethod
    def _get_max_progress(user: Person) -> int:
        # Get parameters
        parameters = (
            models.ExerciseConditions.objects.filter(user=user)  # type: ignore
            .select_related('progress')
            .first()
        )

        # Get 'know' progress value as max progress
        max_progress = (
            parameters.progress.know  # type: ignore
            if parameters and parameters.progress  # type: ignore
            else study_models.ProgressBar.KNOW_DEFAULT
        )
        return max_progress
