"""Word study presenter."""

import logging
from typing import override

from apps.core.storage.clients import DjangoCache
from apps.users.models import CustomUser

from .. import schemas, types
from ..repos.abc import PresentationABC, TranslationRepoABC
from .abc import WordPresentationServiceABC, WordStudyDomainABC

log = logging.getLogger(__name__)


class WordPresentationService(WordPresentationServiceABC):
    """Service to Word study via presentation."""

    def __init__(
        self,
        word_repo: PresentationABC,
        translation_repo: TranslationRepoABC,
        case_storage: DjangoCache[schemas.WordStudyCaseSchema],
        domain: WordStudyDomainABC,
    ) -> None:
        """Construct the service."""
        self._word_repo = word_repo
        self._translation_repo = translation_repo
        self._case_storage = case_storage
        self._domain = domain

    # TODO: Refactor
    @override
    def get_presentation_case(
        self,
        presentation_params: types.WordParamsType,
        user: CustomUser,
    ) -> types.WordCaseType:
        """Get Word study presentation case."""
        candidates = self._word_repo.get_candidates(presentation_params)

        # TODO: Handle exception into view.
        # TODO: Add custom exception?
        if not candidates.translation_ids:
            log.info('No words to study for request params')
            raise LookupError

        case = self._domain.create(candidates)
        schema = schemas.WordStudyCaseSchema(
            translation_id=case.translation_id,
            language='english',
        )
        case_uuid = self._case_storage.set(schema)
        case_data = self._word_repo.get_case(
            user=user,
            translation_id=case.translation_id,
            language='english',
        )

        return types.WordCaseType(
            case_uuid=case_uuid,
            definition=case_data['definition'],
            explanation=case_data['explanation'],
        )
