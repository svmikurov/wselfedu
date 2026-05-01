"""Domain dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from apps.core.domains.exercise import (
    PresentationDomain,
    TestDomain,
    TestExerciseCheckDomain,
)
from apps.core.domains.exercise.deps.selector import (
    CandidatesSelector,
)


class DomainContainer(DeclarativeContainer):
    """Domain dependency injection container."""

    exercise_config = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Exercises
    # =============================================

    candidates_selector = Factory(CandidatesSelector)

    test = Factory(
        TestDomain,
        selector=candidates_selector,
    )
    presentation = Factory(
        PresentationDomain,
        selector=candidates_selector,
    )

    # QUESTION: Deprecated below?

    # -----------------------------------
    # Test exercise domain business logic
    # -----------------------------------

    check_test = Factory(
        TestExerciseCheckDomain,
    )
