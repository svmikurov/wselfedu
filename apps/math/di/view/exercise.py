"""Mathematical discipline view exercise dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Dependency


class ExerciseViewContainer(DeclarativeContainer):
    """Mathematical discipline view exercise dependencies.

    Provides view exercise dependencies for persistent attr injection.
    """

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    handlers = DependenciesContainer()
    assigned_exercises_selector = Dependency()  # type: ignore[var-annotated]

    # -------------------------------------------
    # Dependencies for view persistent references
    # -------------------------------------------

    # REVIEW: Api assigned selection
    api_assigned_selector = assigned_exercises_selector

    api_regular_calculation = handlers.regular_calculation
    api_award_calculation = handlers.award_calculation

    # EXPERIMENTAL: Web calculation exercise
    web_detail_calculation = handlers.web_detail_calculation
    web_regular_calculation = handlers.web_regular_calculation
