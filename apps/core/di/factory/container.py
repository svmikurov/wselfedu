"""Specification factory DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Dict, Factory

from apps.core.adapters.exercise import (
    CreateExerciseSpecFactory,
    UpdateProgressSpecFactory,
)
from contracts.enums import ExerciseAction


class CoreSpecFactoryContainer(DeclarativeContainer):
    """Specification factory DI container."""

    # ===========================================
    # External dependencies
    # ===========================================

    auditor = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Exercise factories
    # ===========================================

    create_exercise = Factory(  # type: ignore[var-annotated]
        CreateExerciseSpecFactory,
        name='Create exercise specification factory.',
    )
    update_progress = Factory(  # type: ignore[var-annotated]
        UpdateProgressSpecFactory,
        name='Update progress specification factory',
    )

    # ===========================================
    # Exercise specification factory registry
    # ===========================================

    presentation_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: create_exercise,
            ExerciseAction.UPDATE_PROGRESS: update_progress,
        },
    )
