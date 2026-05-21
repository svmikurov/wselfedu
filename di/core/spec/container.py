"""Specification factory DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Dict, Factory

from kernel.spec import (
    CheckAnswerSpecFactory,
    CreateExerciseSpecFactory,
    ExplainTaskSpecFactory,
    UpdateProgressSpecFactory,
)
from ports.contract.enums import ExerciseAction


class CoreSpecFactoryContainer(DeclarativeContainer):
    """Specification factory DI container."""

    # ===========================================
    # External dependencies
    # ===========================================

    auditor = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Exercise factories
    # ===========================================

    _create_exercise = Factory(
        CreateExerciseSpecFactory,
        name='Create task specification factory.',
    )
    _check_exercise = Factory(  # type: ignore[var-annotated]
        CheckAnswerSpecFactory,
        name='Check answer specification factory.',
    )
    _update_progress = Factory(  # type: ignore[var-annotated]
        UpdateProgressSpecFactory,
        name='Update progress specification factory',
    )
    _explain_answer = Factory(
        ExplainTaskSpecFactory,
        name='Explain user answer specification factory',
    )

    # ===========================================
    # Exercise specification factory registry
    # ===========================================

    presentation_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: _create_exercise,
            ExerciseAction.UPDATE_PROGRESS: _update_progress,
        },
    )
    test_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: _create_exercise,
            ExerciseAction.CHECK_ANSWER: _check_exercise,
            ExerciseAction.UPDATE_PROGRESS: _update_progress,
            ExerciseAction.EXPLAIN_ANSWER: _explain_answer,
        },
    )
