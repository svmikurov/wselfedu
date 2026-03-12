"""Mathematical discipline web view dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer


class WebViewContainer(DeclarativeContainer):
    """Mathematical discipline web view dependencies."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    handlers = DependenciesContainer()

    # =============================================
    # Student's exercises (assigned by mentor)
    # ---------------------------------------------
    student_exercises = handlers.student_exercises

    # =============================================
    # Calculation exercise
    # ---------------------------------------------
    calculation_exercise_choice = handlers.calculation_exercise_choice
    # Regular
    create_regular_calculation = handlers.create_regular_calculation
    check_regular_calculation = handlers.check_regular_calculation
    # Custom
    start_custom_calculation = handlers.start_custom_calculation
    check_custom_calculation = handlers.check_custom_calculation
    # Mentor's
    start_mentor_calculation = handlers.start_mentor_calculation
    check_mentor_calculation = handlers.check_mentor_calculation
    # Student's
    start_student_calculation = handlers.start_student_calculation
    check_student_calculation = handlers.check_student_calculation
