"""Study settings service."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from .. import models, types
from .abc import StudySettingsRepositoryABC

if TYPE_CHECKING:
    from apps.users.models import Person

# TODO: Refactor


# TODO: Inject repositories
class StudySettingsRepository(StudySettingsRepositoryABC):
    """Provides study repository."""

    @override
    def fetch(self, user: Person) -> types.CaseStudySettingsWEB:
        """Get study settings for presentation case."""
        translation_parameters = models.Parameters.get_instants(user)
        translation_settings = models.TranslationSetting.get_instants(user)
        presentation_settings = models.PresentationSettings.get_instants(user)

        mark = self._get_pk(translation_parameters.mark)
        return types.CaseStudySettingsWEB(
            # Translation parameters
            category=self._get_pk(translation_parameters.category),
            # TODO: Fix mark getting
            mark=[mark] if mark else '[]',  # type: ignore[typeddict-item]
            word_source=self._get_pk(translation_parameters.word_source),
            start_period=self._get_pk(translation_parameters.start_period),
            end_period=self._get_pk(translation_parameters.end_period),
            #
            # - progress phases
            is_study=self._bool_to_str(translation_parameters.is_study),
            is_repeat=self._bool_to_str(translation_parameters.is_repeat),
            is_examine=self._bool_to_str(translation_parameters.is_examine),
            is_know=self._bool_to_str(translation_parameters.is_know),
            #
            # Translation settings
            # TODO: Fix type ignore
            display_order=str(translation_settings.display_order),  # type: ignore[typeddict-item]
            word_count=str(translation_settings.word_count or ''),
            #
            # Presentation settings
            question_timeout=str(presentation_settings.question_timeout or ''),
            answer_timeout=str(presentation_settings.answer_timeout or ''),
        )

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
