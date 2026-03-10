"""Mathematical discipline exercise web handlers."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers.generic import (
    ContextRequestHandler,
    DetailRequestHandler,
    RegularRequestHandler,
    RequestHandler,
)
from apps.core.validators.request.null import NullValidator


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
        RegularRequestHandler,
        validator=NullValidator(),
        use_case=use_cases.calculation_conditions,
        adapter=adapters.calculation_conditions,
    )

    # =============================================
    # Student's exercises (assigned by mentor)
    # ---------------------------------------------
    student_exercises = Factory(
        RequestHandler,
        validator=NullValidator(),
        use_case=use_cases.student_exercises,
        adapter=adapters.student_exercises,
    )

    # =============================================
    # Calculation exercise performing
    # ---------------------------------------------
    create_regular_calculation = Factory(
        RegularRequestHandler,
        validator=validators.create_regular_calculation,
        use_case=use_cases.create_regular_calculation,
        adapter=adapters.create_calculation,
    )
    check_regular_calculation = Factory(
        RegularRequestHandler,
        validator=validators.check_regular_calculation,
        use_case=use_cases.check_regular_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )

    start_custom_calculation = Factory(
        DetailRequestHandler,
        validator=NullValidator(),
        use_case=use_cases.start_custom_calculation,
        adapter=adapters.create_custom_calculation,
    )
    check_custom_calculation = Factory(
        DetailRequestHandler,
        validator=validators.check_custom_calculation,
        use_case=use_cases.check_custom_calculation,
        adapter=adapters.custom_calculation_result_strategy,
    )

    start_student_calculation = Factory(
        ContextRequestHandler,
        validator=NullValidator(),
        use_case=use_cases.start_student_calculation,
        adapter=adapters.create_student_calculation,
    )
    check_student_calculation = Factory(
        ContextRequestHandler,
        validator=validators.check_custom_calculation,
        use_case=use_cases.check_student_calculation,
        adapter=adapters.student_calculation_result_strategy,
    )
