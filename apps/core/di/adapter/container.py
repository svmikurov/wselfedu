"""DI container for adapters."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Dict, Factory

from apps.core.adapters.exercise import (
    CreateExerciseSpecFactory,
    UpdateProgressSpecFactory,
)
from apps.core.adapters.response import (
    PresentationTaskWebAdapter,
    ProcessExerciseAdapterStrategy,
)
from apps.core.adapters.response.null import NullResponseAdapter
from contracts.enums import ExerciseAction, ExerciseStatus

presentation_html: list[str] = [
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
        templates=presentation_html,
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

    # =============================================
    # Presentation exercise strategy
    # =============================================

    presentation_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: Factory(
                CreateExerciseSpecFactory,
                name='Create task specification factory',
            ),
            ExerciseAction.UPDATE_PROGRESS: Factory(
                UpdateProgressSpecFactory,
                name='Update progress specification factory',
            ),
        },
    )
