"""Repository DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.lang import models, repositories
from apps.lang.models import Parameters, TranslationSetting
from apps.lang.repositories.exercise.conditions import (
    RegularParametersRepository,
)


class RepositoryContainer(DeclarativeContainer):
    """Repository DI container."""

    # ----------------
    # English language
    # ----------------

    rule = Factory(
        repositories.RuleRepository,
    )
    translation = Factory(
        repositories.TranslationRepository,
    )

    # ------------------------------------
    # Regular exercise settings repository
    # ------------------------------------

    regular_parameters = Factory(
        RegularParametersRepository,
        parameters_manager=Parameters.objects,
        settings_manager=TranslationSetting.objects,
    )

    study_parameters = Factory(
        repositories.StudyParametersRepository,
    )
    study_settings = Factory(
        repositories.StudySettingsRepository,
    )

    # -----------------
    # Translation study
    # -----------------

    regular_translation_exercise = Factory(
        repositories.TranslationExerciseRepository,
        manager=models.EnglishTranslation.objects,
    )
    detail_translation_exercise = Factory(
        repositories.DetailTranslationRepository,
        manager=models.EnglishTranslation.objects,
    )
    regular_translation_condition = Factory(
        repositories.TranslationConditionsRepository,
        manager=models.EnglishTranslation.objects,
    )

    # ---------------------
    # Progress repositories
    # ---------------------

    regular_translation_progress = Factory(
        repositories.ProgressRepository,
        manager=models.EnglishTranslation.objects,
    )
    assigned_translation_progress = Factory(
        repositories.AssignedTranslationProgressRepository,
    )
