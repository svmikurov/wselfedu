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
    start_detail_calculation = handlers.start_detail_calculation
    check_detail_calculation = handlers.check_detail_calculation
    start_student_calculation = handlers.start_student_calculation
    check_student_calculation = handlers.check_student_calculation
