"""Word study params repository."""

from typing import Any, Literal, override

from django.db import transaction

from apps.core import models as core_models
from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch(self, user: CustomUser) -> types.WordPresentationParamsT:
        """Fetch parameters with parameter choices."""
        # TODO: Fix database query (N+1)? Now 4.
        parameters = models.Params.objects.filter(user=user)
        categories = models.LangCategory.objects.filter(user=user)
        marks = models.LangMark.objects.filter(user=user)
        sources = core_models.Source.objects.filter(user=user)
        periods = core_models.Period.objects

        initial: dict[str, Any] = (
            parameters.values(  # type: ignore[assignment]
                'category__id',
                'category__name',
                'mark__id',
                'mark__name',
                'word_source__id',
                'word_source__name',
                'start_period__id',
                'start_period__name',
                'end_period__id',
                'end_period__name',
                'word_count',
                'question_timeout',
                'answer_timeout',
                'order',
            ).first()
            or {}
        )

        order_value = (
            initial.get('order')
            or models.Params.TranslateChoices.TO_NATIVE.value
        )
        order_choice = models.Params.TranslateChoices(order_value)

        data = {
            # Parameters options
            'categories': list(categories.values('id', 'name')),
            'marks': list(marks.values('id', 'name')),
            'sources': list(sources.values('id', 'name')),
            'periods': list(periods.values('id', 'name')),
            'orders': [
                {'value': value, 'label': label}
                for value, label in models.Params.TranslateChoices.choices
            ],
            # Selected parameter
            'category': None,
            'mark': None,
            'word_source': None,
            'start_period': None,
            'end_period': None,
            'order': {
                'value': order_choice.value,
                'label': order_choice.label,
            },
            # Set parameter
            'word_count': initial.get('word_count'),
            'question_timeout': initial.get('question_timeout'),
            'answer_timeout': initial.get('answer_timeout'),
        }

        if not initial:
            return data  # type: ignore[return-value]

        if initial.get('category__id'):
            data['category'] = {
                'id': initial['category__id'],
                'name': initial['category__name'],
            }
        if initial.get('mark__id'):
            data['mark'] = {
                'id': initial['mark__id'],
                'name': initial['mark__name'],
            }
        if initial.get('word_source__id'):
            data['word_source'] = {
                'id': initial['word_source__id'],
                'name': initial['word_source__name'],
            }
        if initial.get('start_period__id'):
            data['start_period'] = {
                'id': initial['start_period__id'],
                'name': initial['start_period__name'],
            }
        if initial.get('end_period__id'):
            data['end_period'] = {
                'id': initial['end_period__id'],
                'name': initial['end_period__name'],
            }

        return data  # type: ignore[return-value]

    @override
    @transaction.atomic
    def update(
        self,
        user: CustomUser,
        data: types.UpdateParametersT,
    ) -> types.WordPresentationParamsT:
        """Update initial parameters."""
        (
            models.Params.objects.select_for_update()
            .filter(user=user)
            .update(
                # Initial choices
                category=self._get_initial(data, 'category'),
                mark=self._get_initial(data, 'mark'),
                word_source=self._get_initial(data, 'word_source'),
                order=data.get('order')['value']  # type: ignore[index]
                if data.get('order')
                else None,
                start_period=self._get_initial(data, 'start_period'),
                end_period=self._get_initial(data, 'end_period'),
                # Settings
                word_count=data.get('word_count'),
                question_timeout=data.get('question_timeout'),
                answer_timeout=data.get('answer_timeout'),
            )
        )
        return self.fetch(user)

    @staticmethod
    def _get_initial(
        data: types.UpdateParametersT,
        field_name: Literal[
            'category',
            'mark',
            'word_source',
            'start_period',
            'end_period',
        ],
    ) -> int | None:
        """Get new parameter option ID or return None."""
        value: types.IdName | None = data.get(field_name)
        return None if value is None else value['id']
