"""DI container for adapters."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Dict, Factory

from kernel.adapter.null import NullResponseAdapter
from kernel.adapter.response import (
    CreatePresentationWebAdapter,
    ProcessExerciseAdapterStrategy,
)
from kernel.adapter.response.exercise.test.web import (
    WebTestExerciseAdapter,
)
from ports.contract.enums import ExerciseStatus

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
        CreatePresentationWebAdapter,
        templates=PRESENTATION_TEMPLATES,
        auditor=auditor,
        name='Presentation exercise response adapter',
    )
    _test = Factory(
        WebTestExerciseAdapter,
        templates=TEST_TEMPLATES,
        auditor=auditor,
        name='Test exercise response adapter',
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
            ExerciseStatus.WRONG: _null,
        }
    )

    # =============================================
    # Exercise strategy
    # =============================================

    presentation_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        registry=_presentation_registry,
        auditor=auditor,
        name='Presentation exercise response adapter strategy',
    )
    test_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        registry=_test_registry,
        auditor=auditor,
        name='Test exercise response adapter strategy',
    )
