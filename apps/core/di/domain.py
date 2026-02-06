"""Domain dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from ..domain.exercise import (
    DetailTestCreateDomain,
    PresentationDomain,
    RegularTestCreateDomain,
    TestCheckDomain,
)


class DomainContainer(DeclarativeContainer):
    """Domain dependency injection container."""

    exercise_config = Dependency()  # type: ignore[var-annotated]

    # -----------------------------------
    # Test exercise domain business logic
    # -----------------------------------

    create_regular_test = Factory(
        RegularTestCreateDomain,
        config=exercise_config,
    )
    create_detail_test = Factory(
        DetailTestCreateDomain,
        config=exercise_config,
    )
    check_test = Factory(
        TestCheckDomain,
    )

    # ----------------------------------
    # Presentation domain business logic
    # ----------------------------------

    presentation = Factory(
        PresentationDomain,
        config=exercise_config,
    )
