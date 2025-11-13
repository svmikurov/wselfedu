"""Word study repositories."""

import logging

from apps.users.models import CustomUser

from .. import models
from ..types import WordDataType, WordParamsType, WordStudyParams
from .abc import WordStudyRepositoryABC

log = logging.getLogger(__name__)


class WordStudyRepository(WordStudyRepositoryABC):
    """Word study repository."""

    def get_candidates(self, params: WordParamsType) -> WordStudyParams:
        """Get candidates of words to study."""
        # Temporary translations from english to native
        english_word_ids = models.EnglishWord.objects.all().values_list(
            'id', flat=True
        )
        return WordStudyParams(
            translation_ids=list(english_word_ids),
        )

    def get_word_data(
        self,
        english_word_id: int,
        user: CustomUser,
    ) -> WordDataType:
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

        return WordDataType(
            definition=str(translation.english),
            explanation=str(translation.native),
        )
