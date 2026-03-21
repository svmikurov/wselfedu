"""Language discipline exercise service DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.services.exercise.test import DetailTestCreate


class ExerciseServiceContainer(DeclarativeContainer):
    """Language discipline exercise service DI container."""

    repositories = DependenciesContainer()
    domains = DependenciesContainer()
    use_cases = DependenciesContainer()

    case_storage = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Translation test exercise
    # -------------------------------------------
    # Regular translation test exercise
    create_regular_translation_test = Factory(
        DetailTestCreate,
    )
