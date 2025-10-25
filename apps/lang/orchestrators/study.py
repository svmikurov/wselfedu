"""Word study orchestrators."""

import logging

from apps.users.models import CustomUser

from .. import models
from ..types import WordParamsType, WordStudyParams, WordType
from .abc import WordStudyOrchestratorABC

log = logging.getLogger(__name__)


class WordStudyOrchestrator(WordStudyOrchestratorABC):
    """Word study orchestrator."""

    def get_candidates(self, params: WordParamsType) -> WordStudyParams:
        """Get candidates of words to study."""
        query = models.EnglishWord.objects.all()
        ids = query.values_list('id')
        return WordStudyParams(
            ids=list(ids),  # type: ignore[arg-type]
        )

    def get_case(self, english_word_id: int, user: CustomUser) -> WordType:
        """Get translation for exercise case."""
        try:
            translation = models.EnglishTranslation.objects.select_related(
                'native', 'english'
            ).get(
                native_id=english_word_id,
                user=user,
            )
        except models.EnglishTranslation.DoesNotExist:
            log.info('No case for word study params')
            raise

        return WordType(
            definition=str(translation.english),
            explanation=str(translation.native),
        )
