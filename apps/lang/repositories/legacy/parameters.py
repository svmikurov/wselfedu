"""Word study parameters repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, override

from django.db import transaction
from django.db.models import QuerySet

from apps.core import models as models_core
from apps.lang import models
from ports.interfaces.request_data.api.general import IdName
from ports.refactor.lang import types

if TYPE_CHECKING:
    from apps.users.models import Person

    type OptionsT = Literal[
        'category',
        'mark',
        'word_source',
        'start_period',
        'end_period',
        'display_order',
    ]

    OptionsQuerySetT = (
        QuerySet[models.Category]
        | QuerySet[models.Mark]
        | QuerySet[models_core.Source]
        | QuerySet[models_core.Period]
    )


class StudyParametersRepository:
    """Word study params repository."""

    def _get_id_name(self, queryset: OptionsQuerySetT) -> list[IdName]:
        return list(queryset.values('id', 'name'))

    @override
    def get_options(self, user: Person) -> types.OptionsAPI:  # type: ignore
        """Get word study options."""
        categories = models.Category.objects.filter(user=user)
        marks = models.Mark.objects.filter(user=user)
        sources = models_core.Source.objects.filter(user=user).order_by('pk')
        periods = models_core.Period.objects.all()
        orders = models.TranslationConfiguration.TranslateChoices.choices

        return types.OptionsAPI(
            categories=self._get_id_name(categories),
            marks=self._get_id_name(marks),
            sources=self._get_id_name(sources),
            periods=self._get_id_name(periods),
            display_orders=[
                {'code': str(value), 'name': str(label)}  # type: ignore[typeddict-item]
                for value, label in orders
            ],
        )

    @override
    def fetch(self, user: Person) -> types.CaseSettingsAPI:  # type: ignore
        """Fetch parameters with parameter choices."""
        options = self.get_options(user)

        parameters = (
            models.ExerciseConditions.objects.filter(user=user)
            .select_related(
                'category',
                'mark',
                'word_source',
                'start_period',
                'end_period',
            )
            .first()
            or models.ExerciseConditions()
        )

        translation_settings = (
            models.TranslationConfiguration.objects.filter(user=user).first()
            or models.TranslationConfiguration()
        )

        presentation_settings = (
            models.PresentationSettings.objects.filter(user=user).first()
            or models.PresentationSettings()
        )

        order_value, order_label = (
            models.TranslationConfiguration.resolve_order_choice(
                translation_settings.display_order
            )
        )

        mark = parameters.obj_to_id_name('mark')
        data = {
            **options,
            #
            # Translation meta
            'category': parameters.obj_to_id_name('category'),
            'mark': [mark] if mark else [],
            'word_source': parameters.obj_to_id_name('word_source'),
            'start_period': parameters.obj_to_id_name('start_period'),
            'end_period': parameters.obj_to_id_name('end_period'),
            'is_study': parameters.study,
            'is_repeat': parameters.repeat,
            'is_examine': parameters.examine,
            'is_know': parameters.know,
            #
            # Translation settings
            'display_order': {'code': order_value, 'name': order_label},
            'word_count': translation_settings.word_count,
            #
            # Presentation settings
            'question_timeout': presentation_settings.question_timeout,
            'answer_timeout': presentation_settings.answer_timeout,
        }

        return data  # type: ignore[return-value]

    @override
    @transaction.atomic
    def update(  # type: ignore
        self,
        user: Person,
        data: types.CaseParametersAPI,
    ) -> types.CaseSettingsAPI:
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
            'display_order': self._get_identifier(data, 'display_order'),
            'word_count': data.get('word_count'),
        }

        presentation_settings_defaults = {
            'question_timeout': data.get('question_timeout'),
            'answer_timeout': data.get('answer_timeout'),
        }

        (
            models.ExerciseConditions.objects.update_or_create(
                user=user,
                defaults=translation_meta_defaults,
            )
        )
        (
            models.TranslationConfiguration.objects.update_or_create(
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

    # TODO: Fix type ignore
    @staticmethod
    def _get_pk(instance: object) -> str:
        return str(instance.pk) if instance else ''  # type: ignore[attr-defined]

    @staticmethod
    def _bool_to_str(value: bool | None) -> str:
        match value:
            case True:
                return 'true'
            case False:
                return 'false'
            case None:
                return ''
            case _:
                raise TypeError(f'Unsupported type: {type(value).__name__}')

    @staticmethod
    def _get_identifier(
        data: types.CaseParametersAPI,
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
