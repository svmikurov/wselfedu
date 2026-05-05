"""DI container for adapters."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Dict, Factory

from apps.core.adapters.response import (
    PresentationTaskWebAdapter,
    ProcessExerciseAdapterStrategy,
)
from apps.core.adapters.response.null import NullResponseAdapter
from contracts.enums import ExerciseStatus

presentation_oob_htmls: list[str] = [
    'core/exercise/presentation/task.html',
    'core/exercise/presentation/update_progress.html',
]


class ResponseAdaptersContainer(DeclarativeContainer):
    """Core response adapters DI container."""

    # ================================================
    # External dependencies
    # ================================================

    auditor = Dependency()  # type: ignore

    # ================================================
    # Adapters
    # ================================================

    regular_presentation = Factory(
        PresentationTaskWebAdapter,
        oob_templates=presentation_oob_htmls,
        name='Presentation response adapter',
        auditor=auditor,
    )
    null_adapter = Factory(NullResponseAdapter)

    # =============================================
    # Presentation registries
    # =============================================

    presentation_registries = Dict(
        {
            ExerciseStatus.NEW_TASK: regular_presentation,
            ExerciseStatus.UPDATED_PROGRESS: null_adapter,
        },
    )

    # =============================================
    # Presentation exercise strategy
    # =============================================

    presentation_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        registry=presentation_registries,
    )
