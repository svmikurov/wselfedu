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
        user: CustomUser,
        translation_id: int,
        language: types.LanguageType,
    ) -> types.PresentationDict:
        """Get Presentation case."""
        model = models.TRANSLATION_MODELS[language]

        try:
            translation = model.objects.select_related(  # type: ignore[attr-defined]
                'native', 'english'
            ).get(
                pk=translation_id,
                user=user,
            )
        except model.DoesNotExist:  # type: ignore[attr-defined]
            log.info('No case for word study params')
            raise

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise

        return types.PresentationDict(
            definition=str(translation.english),
            explanation=str(translation.native),
        )
