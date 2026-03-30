"""Language discipline response adapters DI."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from apps.core.adapters.response.exercise.strategy import (
    ProcessExerciseAdapterStrategy,
)
from apps.core.domains.exercise.enums import ExerciseStatusEnum


class WebResponseAdapterContainer(DeclarativeContainer):
    """Language discipline response adapters DI."""

    # =============================================
    # Regular translation presentation
    # =============================================

    regular_translation_presentation_registry = Dict(
        {
            ExerciseStatusEnum.NEW_CASE: ...,
        }
    )

    kregular_translation_presentation = Factory(
        ProcessExerciseAdapterStrategy,
        registry=regular_translation_presentation_registry,
    )
