"""Repository DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from apps.core.repositories.progress import ProgressRepository
from apps.lang import models, repositories
from apps.lang.models import ExerciseConditions, TranslationConfiguration
from apps.lang.repositories import (
    RegularParametersRepository,
)
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)


class LanguageRepositoryContainer(DeclarativeContainer):
    """Repository DI container."""

    # =============================================
    # External dependencies
    # =============================================
    storage = Dependency()  # type: ignore

    # =============================================
    # English language
    # =============================================

    rule = Factory(
        repositories.RuleRepository,
    )
    translation = Factory(
        repositories.TranslationRepository,
    )

    # ---------------------------------------------
    # Regular translation exercise parameters
    # ---------------------------------------------
    translation_parameters = Factory(
        RegularParametersRepository,
        parameters_manager=models.ExerciseConditions.objects,
        conf_manager=models.TranslationConfiguration.objects,
    )

    # ---------------------------------------------
    # Regular translation exercise candidates
    # ---------------------------------------------
    translation_candidates = Factory(
        UserTranslationsRepository,
        manager=models.EnglishTranslation.objects,
    )

    # ---------------------------------------------
    # Regular exercise settings repository
    # ---------------------------------------------
    regular_parameters = Factory(
        RegularParametersRepository,
        parameters_manager=ExerciseConditions.objects,
        conf_manager=TranslationConfiguration.objects,
    )

    study_parameters = Factory(
        repositories.StudyParametersRepository,
    )
    study_settings = Factory(
        repositories.StudySettingsRepository,
    )

    # ---------------------------------------------
    # Translation study
    # ---------------------------------------------
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

    # ---------------------------------------------
    # Progress repositories
    # ---------------------------------------------
    regular_translation_progress = Factory(
        ProgressRepository,
        manager=models.EnglishTranslation.objects,
    )
    assigned_translation_progress = Factory(
        repositories.AssignedTranslationProgressRepository,
    )
