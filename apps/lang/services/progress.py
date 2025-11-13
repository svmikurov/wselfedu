"""Update word study progress service."""

import logging
import uuid
from typing import override

from apps.core.storage.clients import DjangoCache
from apps.users.models import CustomUser

from .. import schemas, types
from ..repos.abc import UpdateWordProgressRepoABC
from .abc import WordProgressServiceABC

log = logging.getLogger(__name__)


class UpdateWordProgressService(WordProgressServiceABC):
    """Update word study progress service."""

    def __init__(
        self,
        progress_repo: UpdateWordProgressRepoABC,
        case_storage: DjangoCache[schemas.WordStudyCaseSchema],
        progress_config: schemas.ProgressConfigSchema,
    ) -> None:
        """Construct the service."""
        self._progress_repo = progress_repo
        self._case_storage = case_storage
        self._progress_config = progress_config

    @override
    def update_progress(
        self,
        user: CustomUser,
        case_uuid: uuid.UUID,
        progress_type: types.ProgressType,
    ) -> None:
        """Update word study progress."""
        progress_value = {
            'known': self._progress_config.increment,
            'unknown': self._progress_config.decrement,
        }[progress_type]

        match progress_type:
            case 'known':
                progress_delta = progress_value
            case 'unknown':
                progress_delta = -progress_value

        try:
            case_data: schemas.WordStudyCaseSchema = self._case_storage.pop(
                cache_kay=case_uuid,
            )
        except KeyError as exc:
            log.warning('Case not found in storage: %s', case_uuid)
            raise KeyError(
                f'Exercise not found or already completed: {case_uuid}'
            ) from exc

        try:
            self._progress_repo.update(
                user=user,
                translation_id=case_data.translation_id,
                language=case_data.language,
                progress_delta=progress_delta,
            )
        except Exception as exc:
            log.exception('Unexpected error during progress update: %s', exc)
            raise
