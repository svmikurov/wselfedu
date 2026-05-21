"""Language app service's DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Dict,
    Factory,
)

from kernel.service.exercise import (
    CheckExerciseService,
    CreateExerciseService,
    ExplainAserAnswerService,
)
from kernel.service.progress import UpdateProgressService
from ports.contract.enums.exercise import ExerciseAction


class ServiceContainer(DeclarativeContainer):
    """Service DI container."""

    # =============================================
    # External dependencies
    # =============================================

    domains = DependenciesContainer()
    formatters = DependenciesContainer()
    repositories = DependenciesContainer()

    auditor = Dependency()  # type: ignore

    # =============================================
    # Exercise's services
    # =============================================

    # Presentation
    # - create
    _create_translation_presentation = Factory(
        CreateExerciseService,
        candidates_repository=repositories.translation_candidates,
        domain=domains.create_presentation,
        formatter=formatters.presentation,
        auditor=auditor,
        name='Create translation presentation service',
    )

    # Test
    # - create
    _create_translation_test = Factory(
        CreateExerciseService,
        candidates_repository=repositories.translation_candidates,
        domain=domains.create_test,
        formatter=formatters.test,
        auditor=auditor,
        name='Create translation test exercise service',
    )
    # - check
    _check_translation_test = Factory(  # type: ignore
        CheckExerciseService,
        domain=domains.check_test,
        auditor=auditor,
        name='Check answer on translation test exercise service',
    )

    _translation_progress = Factory(
        UpdateProgressService,
        repository=repositories.regular_translation_progress,
        auditor=auditor,
        name='Update translation study progress service',
    )

    _expalin_test_answer = Factory(  # type: ignore[var-annotated]
        ExplainAserAnswerService,
        domain=domains.explain_test_answer,
        auditor=auditor,
        name='Expalin user answer service',
    )

    # =============================================
    # Exercise service's registries
    # =============================================

    regular_translation_presentation_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: _create_translation_presentation,
            ExerciseAction.UPDATE_PROGRESS: _translation_progress,
        },
    )
    regular_translation_test_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: _create_translation_test,
            ExerciseAction.CHECK_ANSWER: _check_translation_test,
            ExerciseAction.UPDATE_PROGRESS: _translation_progress,
            ExerciseAction.EXPLAIN_TASK: _expalin_test_answer,
        },
    )
