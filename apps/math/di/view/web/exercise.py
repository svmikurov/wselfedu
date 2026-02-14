"""Mathematical discipline web view dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer


class WebViewContainer(DeclarativeContainer):
    """Mathematical discipline web view dependencies."""

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    handlers = DependenciesContainer()

    # -------------------------------------------
    # Calculation exercise
    # -------------------------------------------

    calculation_exercise_choice = handlers.calculation_exercise_choice
    create_regular_calculation = handlers.create_regular_calculation
    check_regular_calculation = handlers.check_regular_calculation
    create_detail_calculation = handlers.create_detail_calculation
    check_detail_calculation = handlers.check_detail_calculation
    create_assigned_calculation = handlers.create_assigned_calculation
    check_assigned_calculation = handlers.check_assigned_calculation
