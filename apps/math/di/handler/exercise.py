"""Mathematical discipline exercise handlers."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core import handlers


class ExerciseHandlerContainer(DeclarativeContainer):
    """Mathematical discipline exercise handlers."""

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    validators = DependenciesContainer()
    use_cases = DependenciesContainer()
    adapters = DependenciesContainer()

    # HACK: Temporary legacy dependencies, implement handlers
    # Delete 'exercises' dependency
    exercises = DependenciesContainer()

    # -------------------------------------------
    # Calculation exercise handlers
    # -------------------------------------------

    web_detail_calculation = Factory(
        handlers.DetailRequestHandler,
        validator=validators.web_calculation,
        use_case=use_cases.detail_calculation,
        adapter=adapters.web_calculation,
    )
    web_regular_calculation = Factory(
        handlers.RegularRequestHandler,
        validator=validators.web_calculation,
        use_case=use_cases.regular_calculation,
        adapter=adapters.web_calculation,
    )

    # HACK: Temporary legacy dependencies, implement handlers
    # Delete dependencies below
    assigned_exercises_selector = exercises.assigned_exercises_selector
    regular_calculation = exercises.regular_calculation
    award_calculation = exercises.award_calculation
