"""Presentation repositories."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.study.models import Progress

from .. import models

if TYPE_CHECKING:
    from apps.users.models import Person

    from .. import schemas, types

    type Parameters = schemas.ParametersModel
    type Translations = QuerySet[models.EnglishTranslation]

log = logging.getLogger(__name__)


def get_period_delta(id: int) -> datetime:
    """Get period delta."""
    today = timezone.now()
    periods: dict[int, datetime] = {
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
        log.error(f'Unsupported edge period identifier: {id}')
        raise


class EnglishTranslation:
    """English word study Presentation repository."""

    @classmethod
    def fetch(cls, user: Person, parameters: Parameters) -> Translations:
        """Get candidates for Translation presentation."""
        return models.EnglishTranslation.objects.filter(
            cls._get_conditions(user, parameters)
        ).distinct()

    @classmethod
    def _get_conditions(cls, user: Person, parameters: Parameters) -> Q:
        """Convert to Q object representation of lookup conditions."""
        conditions = Q(user=user)

        for field, value in parameters.model_dump().items():
            match field, value:
                # - `False` adds a condition to exclude translation.
                # - `True` is the default value for a Boolean
                #    condition field.
                # - None and an empty `list` are field values ​​without
                #   a condition.

                case _, True | None | []:
                    continue

                case 'category', int(id):
                    conditions &= Q(category=id)

                case 'source', int(id):
                    conditions &= Q(source=id)

                case 'mark', list():
                    conditions &= Q(englishmark__mark_id__in=value)

                case 'start_period', int(id):
                    conditions &= Q(created_at__date__gte=get_period_delta(id))

                case 'end_period', int(id):
                    conditions &= Q(created_at__date__lte=get_period_delta(id))

                case (
                    ('is_study' | 'is_repeat' | 'is_examine' | 'is_know'),
                    False,
                ):
                    conditions &= ~cls._get_progress_condition(field)

                case _, _:
                    log.warning(
                        f'Unsupported lookup condition: {field!r}: {value!r}'
                    )
                    continue

        return conditions

    @staticmethod
    def _get_progress_condition(parameter: types.Progress) -> Q:
        """Get translation study progress condition."""
        # TODO: Implement user specific progress
        return Q(progress__in=Progress.DEFAULT_PROGRESS_RANGES[parameter])
