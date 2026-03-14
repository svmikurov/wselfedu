"""Language discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, DependenciesContainer

from apps.lang.di.adapter.adapter import AdapterContainer
from apps.lang.di.handler.exercise.exercises import ExerciseHandlerContainer
from apps.lang.di.repository.repository import RepositoryContainer
from apps.lang.di.repository.storage import StorageContainer
from apps.lang.di.service.service import ServiceContainer
from apps.lang.di.validator.validator import ValidatorContainer
from apps.lang.di.view.container import ViewContainer


class LanguageContainer(DeclarativeContainer):
    """Language discipline DI container."""

    # ===========================================
    # External containers
    # -------------------------------------------
    configuration = DependenciesContainer()
    domains = DependenciesContainer()

    repositories = Container(
        RepositoryContainer,
    )
    storages = Container(
        StorageContainer,
        config=configuration.storage,
    )

    # ===========================================
    # View handler dependencies
    # -------------------------------------------
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

    # ===========================================
    # View handlers
    # -------------------------------------------
    exercise_handlers = Container(
        ExerciseHandlerContainer,
        validators=validators,
        use_cases=use_cases,
        adapters=adapters,
    )

    # ===========================================
    # Persistent references to the view handler
    # -------------------------------------------
    view_container = Container(
        ViewContainer,
        repositories=repositories,
        use_cases=use_cases,
        presentation_handlers=exercise_handlers.presentation,
        test_handlers=exercise_handlers.test_exercise,
    )
