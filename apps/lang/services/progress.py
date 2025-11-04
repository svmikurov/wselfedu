"""Update word study progress service."""

import uuid
from typing import override

from apps.core.storage.clients import DjangoCache

from .. import schemas, types
from ..repositories.abc import UpdateWordProgressRepoABC
from .abc import WordProgressServiceABC


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
    def update(
        self,
        case_uuid: uuid.UUID,
        progress_type: types.ProgressType,
    ) -> None:
        """Update word study progress."""
        case_data: schemas.WordStudyCaseSchema = self._case_storage.pop(
            case_uuid
        )
        self._progress_repo.update(
            case_data.translation_id,
            case_data.language,
            progress_type,
            getattr(self._progress_config, progress_type),
        )
