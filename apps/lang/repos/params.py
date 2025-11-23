"""Word study params repository."""

from typing import Any, Literal, override

from django.db import transaction

from apps.core import models as core_models
from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser

OptionsT = Literal[
    'category', 'mark', 'word_source', 'start_period', 'end_period'
]


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch(self, user: CustomUser) -> types.WordPresentationParamsT:
        """Fetch parameters with parameter choices."""
        # Parameter options
        categories = models.LangCategory.objects.filter(user=user)
        marks = models.LangMark.objects.filter(user=user)
        sources = core_models.Source.objects.filter(user=user)
        periods = core_models.Period.objects

        # Default, selected and set parameters
        parameters = models.Params.objects.filter(user=user)

        custom: dict[str, Any] = (
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

        order_value, order_label = models.Params.resolve_order_choice(
            custom.get('order')
        )

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
            #
            # Selected parameter default
            'category': None,
            'mark': None,
            'word_source': None,
            'start_period': None,
            'end_period': None,
            'order': {'value': order_value, 'label': order_label},
            #
            # The parameters set, if any
            'word_count': custom.get('word_count'),
            'question_timeout': custom.get('question_timeout'),
            'answer_timeout': custom.get('answer_timeout'),
        }

        # Provides default parameters if the
        # user has not set them themselves.
        if not custom:
            return data  # type: ignore[return-value]

        # Selected parameters set by the user
        data['category'] = self._build_option(custom, 'category')
        data['mark'] = self._build_option(custom, 'mark')
        data['word_source'] = self._build_option(custom, 'word_source')
        data['start_period'] = self._build_option(custom, 'start_period')
        data['end_period'] = self._build_option(custom, 'end_period')

        return data  # type: ignore[return-value]

    @staticmethod
    def _build_option(
        data: dict[str, Any],
        field_name: str,
    ) -> types.IdName | None:
        """Build id-name option."""
        id_field, name_field = f'{field_name}__id', f'{field_name}__name'
        return (
            {'id': data[id_field], 'name': data[name_field]}
            if data.get(id_field)
            else None
        )

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
                #
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
        field_name: OptionsT,
    ) -> int | None:
        """Get new parameter option ID or return None."""
        value: types.IdName | None = data.get(field_name)
        return None if value is None else value['id']
