"""Word study params repository."""

from typing import Any, Literal, override

from django.db import transaction

from apps.core import models as models_core
from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import Person

OptionsT = Literal[
    'category',
    'mark',
    'word_source',
    'start_period',
    'end_period',
    'translation_order',
]


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch(self, user: Person) -> types.SetStudyParameters:
        """Fetch parameters with parameter choices."""
        # Parameter options
        categories = models.LangCategory.objects.filter(user=user)
        marks = models.LangMark.objects.filter(user=user)
        sources = models_core.Source.objects.filter(user=user)
        periods = models_core.Period.objects

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
                'translation_order',
            ).first()
            or {}
        )

        order_value, order_label = models.Params.resolve_order_choice(
            custom.get('translation_order')
        )

        data = {
            # Parameters options
            'categories': list(categories.values('id', 'name')),
            'marks': list(marks.values('id', 'name')),
            'sources': list(sources.values('id', 'name')),
            'periods': list(periods.values('id', 'name')),
            'translation_orders': [
                {'code': value, 'name': label}
                for value, label in models.Params.TranslateChoices.choices
            ],
            #
            # Selected parameter default
            'category': None,
            'mark': None,
            'word_source': None,
            'start_period': None,
            'end_period': None,
            'translation_order': {'code': order_value, 'name': order_label},
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
        user: Person,
        data: types.StudyParameters,
    ) -> types.SetStudyParameters:
        """Update initial parameters."""
        defaults = {
            'category_id': self._get_identifier(data, 'category'),
            'mark_id': self._get_identifier(data, 'mark'),
            'word_source_id': self._get_identifier(data, 'word_source'),
            'translation_order': self._get_identifier(
                data, 'translation_order'
            ),
            'start_period_id': self._get_identifier(data, 'start_period'),
            'end_period_id': self._get_identifier(data, 'end_period'),
            'word_count': data.get('word_count'),
            'question_timeout': data.get('question_timeout'),
            'answer_timeout': data.get('answer_timeout'),
        }
        (
            models.Params.objects.update_or_create(
                user=user,
                defaults=defaults,
            )
        )
        return self.fetch(user)

    @staticmethod
    def _get_identifier(
        data: types.WordParameters,
        field_name: OptionsT,
    ) -> int | str | None:
        """Get parameter identifier or return None."""
        match data.get(field_name):
            case {'id': int(id), 'name': _}:
                return id
            case {'code': str(code), 'name': _}:
                return code
            case _:
                return None
