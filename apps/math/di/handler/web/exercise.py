"""Mathematical discipline exercise web handlers."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers.generic import (
    RequestHandler,
)
from apps.core.parsers.request import NullParser
from apps.core.validators.request.null import NullValidator
from apps.math.handlers.types import StudentExerciseListHandler
from apps.math.parsers.exercise import CalculationParser


class ExerciseWebHandlerContainer(DeclarativeContainer):
    """Mathematical discipline exercise web handlers."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    validators = DependenciesContainer()
    use_cases = DependenciesContainer()
    adapters = DependenciesContainer()

    # =============================================
    # Calculation exercise conditions
    # ---------------------------------------------
    # Provides:
    # - form for calculation conditions
    # - table of user's saved calculation conditions
    #   (not yet implemented)
    # - table of assigned by mentor calculation exercises
    #   (not yet implemented)
    # Allows start exercise with selected conditions.
    calculation_exercise_choice = Factory(
        StudentExerciseListHandler,
        parser=Factory(NullParser),
        validator=Factory(NullValidator),
        use_case=use_cases.calculation_conditions,
        adapter=adapters.calculation_conditions,
    )

    # =============================================
    # Student's exercises (assigned by mentor)
    # ---------------------------------------------
    student_exercises = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=Factory(NullValidator),
        use_case=use_cases.student_exercises,
        adapter=adapters.student_exercises,
    )

    # =============================================
    # Calculation exercise performing
    # ---------------------------------------------
    # Regular calculation have no milestone
    create_regular_calculation = Factory(
        RequestHandler,
        parser=Factory(CalculationParser),
        validator=Factory(NullValidator),
        use_case=use_cases.create_regular_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_regular_calculation = Factory(
        RequestHandler,
        parser=Factory(CalculationParser),
        validator=validators.check_custom_calculation,
        use_case=use_cases.check_regular_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )

    # Custom calculation have owner's milestone
    start_custom_calculation = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=Factory(NullValidator),
        use_case=use_cases.start_custom_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_custom_calculation = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=validators.check_custom_calculation,
        use_case=use_cases.check_custom_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )

    # Mentor may run assigned to student the calculation exercise
    # by itself.
    # Mentor's calculation have no milestone for mentor.
    start_mentor_calculation = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=Factory(NullValidator),
        use_case=use_cases.start_mentor_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_mentor_calculation = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=validators.check_custom_calculation,
        use_case=use_cases.check_mentor_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )

    # Student's calculation have milestone from mentor
    start_student_calculation = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=Factory(NullValidator),
        use_case=use_cases.start_student_calculation,
        adapter=adapters.create_student_calculation,
    )
    check_student_calculation = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=validators.check_custom_calculation,
        use_case=use_cases.check_student_calculation,
        adapter=adapters.student_calculation_result_strategy,
    )
