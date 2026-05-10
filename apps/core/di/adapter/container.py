"""DI container for adapters."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Dict, Factory

from apps.core.adapters.response import (
    NullResponseAdapter,
    PresentationTaskWebAdapter,
    ProcessExerciseAdapterStrategy,
)
from apps.core.adapters.response.exercise.test.web import (
    WebTestExerciseAdapter,
)
from contracts.enums import ExerciseStatus

PRESENTATION_TEMPLATES: tuple[str, ...] = (
    'core/exercise/presentation/task.html',
    'core/exercise/presentation/update_progress.html',
)
TEST_TEMPLATES: tuple[str] = ('core/exercise/test/task.html',)


class ResponseAdaptersContainer(DeclarativeContainer):
    """Core response adapters DI container."""

    # ================================================
    # External dependency
    # ================================================

    auditor = Dependency()  # type: ignore

    # ================================================
    # Exercise action result response adapter
    # ================================================

    _null = Factory(NullResponseAdapter)

    _presentation = Factory(
        PresentationTaskWebAdapter,
        templates=PRESENTATION_TEMPLATES,
        name='Presentation response adapter',
        auditor=auditor,
    )
    _test = Factory(
        WebTestExerciseAdapter,
        templates=TEST_TEMPLATES,
        name='Test exercise response adapter',
        auditor=auditor,
    )

    # =============================================
    # Exercise registry
    # =============================================

    _presentation_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: _presentation,
            ExerciseStatus.UPDATED_PROGRESS: _null,
        },
    )

    _test_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: _test,
            ExerciseStatus.UPDATED_PROGRESS: _null,
            ExerciseStatus.CORRECT: _null,
        }
    )

    # =============================================
    # Exercise strategy
    # =============================================

    presentation_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        registry=_presentation_registry,
    )
    test_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        registry=_test_registry,
    )
