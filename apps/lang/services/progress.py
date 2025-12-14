"""Update word study progress service."""

import logging
from typing import override

from apps.core.storage import services as storage
from apps.users.models import Person

from .. import schemas, types
from ..repositories.abc import ProgressABC
from .abc import WordProgressServiceABC

log = logging.getLogger(__name__)


class UpdateWordProgressService(WordProgressServiceABC):
    """Update word study progress service."""

    def __init__(
        self,
        progress_repo: ProgressABC,
        case_storage: storage.TaskStorage[schemas.WordStudyStoredCase],
        progress_config: schemas.ProgressConfigSchema,
    ) -> None:
        """Construct the service."""
        self._progress_repo = progress_repo
        self._case_storage = case_storage
        self._progress_config = progress_config

    @override
    def update_progress(
        self,
        user: Person,
        data: types.ProgressCase,
    ) -> None:
        """Update word study progress."""
        case_uuid = data['case_uuid']
        is_known = data['is_known']

        progress_delta = {
            True: self._progress_config.increment,
            False: -self._progress_config.decrement,
        }[is_known]

        try:
            case_data: schemas.WordStudyStoredCase = (
                self._case_storage.retrieve_task(uid=data['case_uuid'])
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
