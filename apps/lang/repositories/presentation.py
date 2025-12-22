"""Word study repositories."""

import logging
from datetime import datetime, timedelta
from typing import override

from django.db.models import Q
from django.utils import timezone

from apps.users.models import Person

from .. import models, types
from .abc import PresentationABC

log = logging.getLogger(__name__)


def get_period(id: int) -> datetime | None:
    """Get edge period."""
    today = timezone.now()
    periods = {
        1: today,
        2: today - timedelta(days=1),
        3: today - timedelta(days=2),
        4: today - timedelta(days=3),
        5: today - timedelta(days=5),
        6: today - timedelta(weeks=1),
        7: today - timedelta(weeks=2),
        8: today - timedelta(weeks=3),
        9: today - timedelta(weeks=5),
        10: today - timedelta(weeks=13),
        11: today - timedelta(weeks=26),
        12: today - timedelta(weeks=52),
    }

    try:
        return periods[id]
    except KeyError:
        log.error(f'Unsupported edge period id: {id}')
        raise


class EnglishPresentation(PresentationABC):
    """English word study Presentation repository."""

    @override
    def get_candidates(
        self,
        parameters: types.CaseParameters,
    ) -> types.CaseCandidates:
        """Get candidates for Presentation."""
        english_word_ids = models.EnglishTranslation.objects.filter(
            self._get_conditions(parameters)
        ).values_list('id', flat=True)

        return types.CaseCandidates(
            translation_ids=list(english_word_ids),
        )

    @override
    def get_translation(
        self,
        user: Person,
        translation_id: int,
    ) -> types.PresentationDataT:
        """Get Presentation case."""
        try:
            translation = (
                models.EnglishTranslation.objects.filter(
                    user=user,
                    id=translation_id,
                )
                .select_related('native', 'english')
                .get()
            )

        except models.EnglishTranslation.DoesNotExist:
            log.info('No case for word study params')
            raise

        except Exception as exc:
            log.error(f'Unexpected error: {exc}')
            raise

        return self._build_case(translation)

    @staticmethod
    def _build_case(
        translation: models.EnglishTranslation,
    ) -> types.PresentationDataT:
        return {
            'definition': translation.english.word,
            'explanation': translation.native.word,
            'info': {
                'progress': translation.progress,
            },
        }

    @staticmethod
    def _get_conditions(
        parameters_db_data: types.TranslationParameters,
    ) -> Q:
        """Convert parameters to Q object represents of conditions."""
        conditions = Q()

        for key, value in parameters_db_data.items():
            match key, value:
                case _, None:
                    continue

                case 'category', {'id': int(id), 'name': _}:
                    conditions &= Q(category=id)

                case 'mark', {'id': int(id), 'name': _}:
                    conditions &= Q(marks=id)

                case 'word_source', {'id': int(id), 'name': _}:
                    conditions &= Q(source=id)

                case 'start_period', {'id': int(id), 'name': _}:
                    conditions &= Q(created_at__date__gte=get_period(id))

                case 'end_period', {'id': int(id), 'name': _}:
                    conditions &= Q(created_at__date__lte=get_period(id))

                # TODO: Fix
                case 'translation_order', {'code': _, 'name': _}:
                    pass

                case _, _:
                    log.warning(
                        f'Unsupported lookup condition: {key!r}: {value!r}'
                    )
                    continue

        return conditions
