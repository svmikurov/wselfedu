"""Word study service."""

import logging
import uuid
from typing import override

from apps.core.storage.clients import DjangoCache
from apps.users.models import CustomUser

from .. import schemas, types
from ..repos.abc import PresentationABC
from .abc import WordPresentationServiceABC, WordStudyDomainABC

log = logging.getLogger(__name__)


class WordPresentationService(WordPresentationServiceABC):
    """Service to Word study via presentation."""

    def __init__(
        self,
        word_repo: PresentationABC,
        case_storage: DjangoCache[schemas.WordStudyStoredCase],
        domain: WordStudyDomainABC,
    ) -> None:
        """Construct the service."""
        self._word_repo = word_repo
        self._case_storage = case_storage
        self._domain = domain

    # TODO: Refactor
    @override
    def get_presentation_case(
        self,
        user: CustomUser,
        presentation_params: types.ParamsChoicesT,
    ) -> types.PresentationCaseT:
        """Get Word study presentation case."""
        candidates = self._word_repo.get_candidates(presentation_params)

        # TODO: Handle exception into view.
        # TODO: Add custom exception?
        if not candidates.translation_ids:
            log.info('No words to study for request params')
            raise LookupError

        case = self._domain.create(candidates)
        case_uuid = self._store_case(case)
        case_data = self._word_repo.get_case(
            user=user,
            translation_id=case.translation_id,
            language='english',
        )

        return self._build_case_data(case_uuid, case_data)

    def _store_case(self, case: types.WordStudyCase) -> uuid.UUID:
        schema = schemas.WordStudyStoredCase(
            translation_id=case.translation_id,
            language='english',
        )
        case_uuid = self._case_storage.set(schema)
        return case_uuid

    # TODO: Fix type ignore
    @staticmethod
    def _build_case_data(
        case_uuid: uuid.UUID,
        case_data: types.PresentationDataT,
    ) -> types.PresentationCaseT:
        """Build Presentation case."""
        case: types.PresentationCaseT = {
            'case_uuid': case_uuid,
            'definition': case_data['definition'],
            'explanation': case_data['explanation'],
            'info': {
                'progress': case_data['info']['progress'],  # type: ignore[typeddict-item, index]
            },
        }
        return case
