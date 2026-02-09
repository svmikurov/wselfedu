"""View-injected dependencies container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, DependenciesContainer

from .exercise import ViewExerciseContainer


class ViewContainer(DeclarativeContainer):
    """Container providing view-injected dependencies."""

    # Exercise services & repositories
    use_cases = DependenciesContainer()
    repositories = DependenciesContainer()

    # Exercise dependencies
    presentation_handlers = DependenciesContainer()
    test_handlers = DependenciesContainer()

    # -------------------------------------------
    # Dependency container
    # -------------------------------------------

    exercise = Container(
        ViewExerciseContainer,
        use_cases=use_cases,
        repositories=repositories,
        presentation_handlers=presentation_handlers,
        test_handlers=test_handlers,
    )

    # -------------------------------------------
    # Dependency
    # -------------------------------------------

    english_translation = repositories.translation
