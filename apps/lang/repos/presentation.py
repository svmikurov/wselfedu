"""Word study repositories."""

import logging

from django.db.models import IntegerField, OuterRef, Subquery

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
        translation_model = models.TRANSLATION_MODELS[language]
        progress_model = models.PROGRESS_MODELS[language]

        try:
            progress_subquery = progress_model.objects.filter(  # type: ignore[attr-defined]
                translation_id=OuterRef('id'), user=user
            ).values('progress')[:1]

            translation_data = (
                translation_model.objects.filter(  # type: ignore[attr-defined]
                    id=translation_id,
                    user=user,
                )
                .select_related('native', 'english')
                .annotate(
                    user_progress=Subquery(
                        progress_subquery,
                        output_field=IntegerField(),
                    )
                )
                .get()
            )

        except translation_model.DoesNotExist:  # type: ignore[attr-defined]
            log.info('No case for word study params')
            raise

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise

        return types.PresentationDict(
            definition=translation_data.english.word,
            explanation=translation_data.native.word,
            progress=translation_data.user_progress,
        )
