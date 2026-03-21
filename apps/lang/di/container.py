"""Language discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Dependency

from .adapter.web.container import WebAdapterContainer
from .handler.web.container import WebHandlerContainer
from .repository.repository import RepositoryContainer
from .service.container import ExerciseServiceContainer
from .use_case.container import UseCaseContainer


class LanguageContainer(DeclarativeContainer):
    """Language discipline DI container."""

    # ===========================================
    # External dependencies
    # -------------------------------------------
    storage = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Internal dependencies
    # -------------------------------------------
    repositories = Container(
        RepositoryContainer,
        storage=storage,
    )
    exercise_services = Container(
        ExerciseServiceContainer,
    )

    # ===========================================
    # View handler dependencies
    # -------------------------------------------
    use_cases = Container(
        UseCaseContainer,
        storage=storage,
        exercise_services=exercise_services,
    )
    web_adapters = Container(
        WebAdapterContainer,
    )

    # ===========================================
    # View handlers
    # -------------------------------------------
    web_handlers = Container(
        WebHandlerContainer,
        use_cases=use_cases,
        adapters=web_adapters,
        storage=storage,
    )
