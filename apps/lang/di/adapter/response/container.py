"""Language discipline response adapters DI."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from apps.core.adapters.response.exercise.strategy import (
    ProcessExerciseAdapterStrategy,
)
from interfaces.enums import ExerciseStatus


class WebResponseAdapterContainer(DeclarativeContainer):
    """Language discipline response adapters DI."""

    # =============================================
    # Regular translation presentation
    # =============================================

    regular_translation_presentation_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: ...,
        }
    )

    regular_translation_presentation = Factory(
        ProcessExerciseAdapterStrategy,
        registry=regular_translation_presentation_registry,
    )
