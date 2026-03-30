"""Domain dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from apps.core.domains.exercise import (
    PresentationDomain,
    TestExerciseCheckDomain,
)


class DomainContainer(DeclarativeContainer):
    """Domain dependency injection container."""

    exercise_config = Dependency()  # type: ignore[var-annotated]

    # -----------------------------------
    # Test exercise domain business logic
    # -----------------------------------

    check_test = Factory(
        TestExerciseCheckDomain,
    )

    # ----------------------------------
    # Presentation domain business logic
    # ----------------------------------

    presentation = Factory(
        PresentationDomain,
        config=exercise_config,
    )
