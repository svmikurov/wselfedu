"""Word study parameters repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeAlias, override

from django.db import transaction
from django.db.models import QuerySet

from apps.core import models as models_core
from apps.lang import models, types
from apps.lang.repositories.abc import WordStudyParamsRepositoryABC

if TYPE_CHECKING:
    from apps.users.models import Person

OptionsT: TypeAlias = Literal[
    'category',
    'mark',
    'word_source',
    'start_period',
    'end_period',
    'translation_order',
]

OptionsQuerySetT: TypeAlias = QuerySet[
    models.LangCategory
    | models.LangMark
    | models_core.Source
    | models_core.Period
]


class WordStudyParametersRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    def _get_id_name(self, queryset: OptionsQuerySetT) -> list[types.IdName]:
        return list(queryset.values('id', 'name'))  # type: ignore[arg-type]

    @override
    def get_options(self, user: Person) -> types.Options:
        """Get word study options."""
        categories = models.LangCategory.objects.filter(user=user)
        marks = models.LangMark.objects.filter(user=user)
        sources = models_core.Source.objects.filter(user=user)
        periods = models_core.Period.objects.all()
        orders = models.TranslationSetting.TranslateChoices.choices

        return types.Options(
            categories=self._get_id_name(categories),
            marks=self._get_id_name(marks),
            sources=self._get_id_name(sources),
            periods=self._get_id_name(periods),
            translation_orders=[
                {'code': str(value), 'name': str(label)}
                for value, label in orders
            ],
        )

    @override
    def fetch(self, user: Person) -> types.SetStudyParameters:
        """Fetch parameters with parameter choices."""
        options = self.get_options(user)

        parameters = (
            models.Parameters.objects.filter(user=user)
            .select_related(
                'category',
                'mark',
                'word_source',
                'start_period',
                'end_period',
            )
            .first()
            or models.Parameters()
        )

        translation_settings = (
            models.TranslationSetting.objects.filter(user=user).first()
            or models.TranslationSetting()
        )

        presentation_settings = (
            models.PresentationSettings.objects.filter(user=user).first()
            or models.PresentationSettings()
        )

        order_value, order_label = (
            models.TranslationSetting.resolve_order_choice(
                translation_settings.translation_order
            )
        )

        data = {
            **options,
            #
            # Translation meta
            'category': parameters.obj_to_id_name('category'),
            'mark': parameters.obj_to_id_name('mark'),
            'word_source': parameters.obj_to_id_name('word_source'),
            'start_period': parameters.obj_to_id_name('start_period'),
            'end_period': parameters.obj_to_id_name('end_period'),
            'is_study': parameters.study,
            'is_repeat': parameters.repeat,
            'is_examine': parameters.examine,
            'is_know': parameters.know,
            #
            # Translation settings
            'translation_order': {'code': order_value, 'name': order_label},
            'word_count': translation_settings.word_count,
            #
            # Presentation settings
            'question_timeout': presentation_settings.question_timeout,
            'answer_timeout': presentation_settings.answer_timeout,
        }

        return data  # type: ignore[return-value]

    @override
    @transaction.atomic
    def update(
        self,
        user: Person,
        data: types.WordParameters,
    ) -> types.SetStudyParameters:
        """Update initial parameters."""
        translation_meta_defaults = {
            'category_id': self._get_identifier(data, 'category'),
            'mark_id': self._get_identifier(data, 'mark'),
            'word_source_id': self._get_identifier(data, 'word_source'),
            'start_period_id': self._get_identifier(data, 'start_period'),
            'end_period_id': self._get_identifier(data, 'end_period'),
            'is_study': data.get('is_study'),
            'is_repeat': data.get('is_repeat'),
            'is_examine': data.get('is_examine'),
            'is_know': data.get('is_know'),
        }

        translation_settings_defaults = {
            'translation_order': self._get_identifier(
                data, 'translation_order'
            ),
            'word_count': data.get('word_count'),
        }

        presentation_settings_defaults = {
            'question_timeout': data.get('question_timeout'),
            'answer_timeout': data.get('answer_timeout'),
        }

        (
            models.Parameters.objects.update_or_create(
                user=user,
                defaults=translation_meta_defaults,
            )
        )
        (
            models.TranslationSetting.objects.update_or_create(
                user=user,
                defaults=translation_settings_defaults,
            )
        )
        (
            models.PresentationSettings.objects.update_or_create(
                user=user,
                defaults=presentation_settings_defaults,
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
