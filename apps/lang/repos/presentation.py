"""Word study repositories."""

import logging

from apps.users.models import CustomUser

from .. import models, types
from .abc import PresentationABC

log = logging.getLogger(__name__)


class Presentation(PresentationABC):
    """Word study Presentation repo."""

    def get_candidates(
        self,
        params: types.WordParamsType,
    ) -> types.WordStudyParams:
        """Get candidates for Presentation."""
        # Temporary translations from english to native
        english_word_ids = models.EnglishWord.objects.all().values_list(
            'id', flat=True
        )
        return types.WordStudyParams(
            translation_ids=list(english_word_ids),
        )

    def get_case(
        self,
        english_word_id: int,
        user: CustomUser,
    ) -> types.WordDataType:
        """Get Presentation case."""
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

        return types.WordDataType(
            definition=str(translation.english),
            explanation=str(translation.native),
        )
