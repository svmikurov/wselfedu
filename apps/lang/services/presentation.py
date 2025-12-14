"""Word study service."""

import logging
import uuid
from typing import override

from apps.core.exceptions import info
from apps.core.storage import services as storage
from apps.users.models import Person

from .. import domain, repositories, schemas, types
from .abc import WordPresentationServiceABC

log = logging.getLogger(__name__)


class WordPresentationService(WordPresentationServiceABC):
    """Word study Presentation service."""

    def __init__(
        self,
        word_repo: repositories.PresentationABC,
        case_storage: storage.TaskStorage[schemas.WordStudyStoredCase],
        domain: domain.WordStudyDomainABC,
    ) -> None:
        """Construct the service."""
        self._word_repo = word_repo
        self._case_storage = case_storage
        self._domain = domain

    # TODO: Refactor
    @override
    def get_presentation_case(
        self,
        user: Person,
        presentation_params: types.WordParameters,
    ) -> types.PresentationCaseT:
        """Get Word study presentation case."""
        candidates = self._word_repo.get_candidates(presentation_params)

        if not candidates.translation_ids:
            log.info('No translation to study for requested parameters')
            raise info.NoTranslationsAvailableException

        case = self._domain.create(candidates)
        case_uuid = self._store_case(case)
        case_data = self._word_repo.get_word_study_data(
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
        case_uuid = self._case_storage.save_task(schema)
        return case_uuid

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
                'progress': case_data['info']['progress'],
            },
        }
        return case
