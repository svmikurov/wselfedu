"""Mathematical discipline exercise web handlers."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.validators.request.null import NullValidator
from apps.math.handlers.types import StudentExerciseListHandler
from apps.math.parsers.exercise import CalculationParser
from kernel.assembler.impl import (
    DetailQueryContextAssembler,
    UserAssembler,
    UserDetailAssembler,
    UserDetailDataAssembler,
    UserQueryAssembler,
    UserQueryDataAssembler,
)
from kernel.handler.generic import RequestHandler


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
        validator=Factory(NullValidator),
        assembler=Factory(DetailQueryContextAssembler),
        use_case=use_cases.calculation_conditions,
        adapter=adapters.calculation_conditions,
    )

    # =============================================
    # Student's exercise list (assigned by mentor)
    # ---------------------------------------------
    student_calculation_list = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=use_cases.student_exercises,
        adapter=adapters.student_exercises,
    )

    # =============================================
    # Calculation exercise performing
    # ---------------------------------------------
    # Regular calculation have no milestone
    create_regular_calculation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(
            UserQueryAssembler,
            parser=Factory(CalculationParser),
        ),
        use_case=use_cases.create_regular_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_regular_calculation = Factory(
        RequestHandler,
        validator=validators.check_custom_calculation,
        assembler=Factory(
            UserQueryDataAssembler,
            parser=Factory(CalculationParser),
        ),
        use_case=use_cases.check_regular_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )
    # ---------------------------------------------
    # Custom calculation have owner's milestone
    start_custom_calculation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserDetailAssembler),
        use_case=use_cases.start_custom_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_custom_calculation = Factory(
        RequestHandler,
        validator=validators.check_custom_calculation,
        assembler=Factory(UserDetailDataAssembler),
        use_case=use_cases.check_custom_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )
    # ---------------------------------------------
    # Mentor may run assigned to student the calculation exercise
    # by itself.
    # Mentor's calculation have no milestone for mentor.
    start_mentor_calculation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserDetailDataAssembler),
        use_case=use_cases.start_mentor_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_mentor_calculation = Factory(
        RequestHandler,
        validator=validators.check_custom_calculation,
        assembler=Factory(UserDetailDataAssembler),
        use_case=use_cases.check_mentor_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )
    # ---------------------------------------------
    # Student's calculation have milestone from mentor
    start_student_calculation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserDetailDataAssembler),
        use_case=use_cases.start_student_calculation,
        adapter=adapters.create_student_calculation,
    )
    check_student_calculation = Factory(
        RequestHandler,
        validator=validators.check_custom_calculation,
        assembler=Factory(UserDetailDataAssembler),
        use_case=use_cases.check_student_calculation,
        adapter=adapters.student_calculation_result_strategy,
    )
