"""Domain dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from kernel.domain.exercise import (
    CandidatesSelector,
    ExplainTestAnswerDomain,
    PresentationDomain,
    TestDomain,
    TestExerciseCheckDomain,
)


class DomainContainer(DeclarativeContainer):
    """Domain dependency injection container."""

    # =============================================
    # External dependency
    # =============================================

    exercise_config = Dependency()  # type: ignore[var-annotated]
    auditor = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Exercises
    # =============================================

    candidates_selector = Factory(CandidatesSelector)

    # Presentation exercise
    # ---------------------

    create_presentation = Factory(
        PresentationDomain,
        selector=candidates_selector,
    )

    # Test exercise
    # -------------

    create_test = Factory(
        TestDomain,
        selector=candidates_selector,
    )
    check_test = Factory(
        TestExerciseCheckDomain,
        auditor=auditor,
        name='Check user answer on test exercise domain',
    )
    explain_test_answer = Factory(
        ExplainTestAnswerDomain,
        auditor=auditor,
        name='Explain user test answer domain',
    )
