"""Language discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, DependenciesContainer

from .adapter import AdapterContainer
from .handler.exercise.exercises import ExerciseHandlerContainer
from .repository import RepositoryContainer
from .storage import StorageContainer
from .use_case import ServiceContainer
from .validator import ValidatorContainer
from .view.container import ViewContainer


class LanguageContainer(DeclarativeContainer):
    """Language discipline DI container."""

    configuration = DependenciesContainer()
    domains = DependenciesContainer()

    repositories = Container(
        RepositoryContainer,
    )
    storages = Container(
        StorageContainer,
        config=configuration.storage,
    )

    validators = Container(
        ValidatorContainer,
    )
    use_cases = Container(
        ServiceContainer,
        exercise_config=configuration.exercise,
        progress_config=configuration.progress,
        repositories=repositories,
        domains=domains,
        case_storage=storages.exercise_case_storage,
    )
    adapters = Container(
        AdapterContainer,
    )

    # -------------------------
    # Exercise request handlers
    # -------------------------

    exercise_handlers = Container(
        ExerciseHandlerContainer,
        validators=validators,
        use_cases=use_cases,
        adapters=adapters,
    )

    # -------------------------
    # View dependency injection
    # -------------------------

    view_container = Container(
        ViewContainer,
        repositories=repositories,
        use_cases=use_cases,
        presentation_handlers=exercise_handlers.presentation,
        test_handlers=exercise_handlers.test_exercise,
    )
