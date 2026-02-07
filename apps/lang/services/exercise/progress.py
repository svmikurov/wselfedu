"""Update word study progress service."""

import logging
from typing import override

from apps.core.domain.exercise import ProgressConfigSchema
from apps.core.storage import services as storage
from apps.lang import types
from apps.lang.repositories.abc import ProgressRepositoryABC
from apps.lang.schemas import dto
from apps.users.models import Person

from .abc import WordProgressServiceABC

log = logging.getLogger(__name__)


class ProgressService(WordProgressServiceABC):
    """Update regular translation study progress service."""

    def __init__(
        self,
        repository: ProgressRepositoryABC,
        case_storage: storage.TaskStorage[dto.CaseMeta],
        config: ProgressConfigSchema,
    ) -> None:
        """Construct the service."""
        self._repository = repository
        self._case_storage = case_storage
        self._config = config

    @override
    def update_progress(
        self,
        user: Person,
        data: types.ProgressCase,
    ) -> None:
        """Update word study progress."""
        case_uuid = data['case_uuid']
        is_known = data['is_known']

        delta = {
            True: self._config.increment,
            False: -self._config.decrement,
        }[is_known]

        try:
            case_meta: dto.CaseMeta = self._case_storage.retrieve_task(
                uid=data['case_uuid']
            )
        except KeyError as exc:
            log.warning('Case not found in storage: %s', case_uuid)
            raise KeyError(
                f'Exercise not found or already completed: {case_uuid}'
            ) from exc

        try:
            self._repository.update(user=user, pk=case_meta.pk, delta=delta)
        except Exception as exc:
            log.exception('Unexpected error during progress update: %s', exc)
            raise
