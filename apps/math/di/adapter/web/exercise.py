"""Mathematical discipline web adapter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.core.adapters.response.exercise.strategy import (
    ProcessExerciseAdapterStrategy,
)
from apps.math.adapters.response.web import exercise as adapters


class ExerciseWebAdapterContainer(DeclarativeContainer):
    """Mathematical discipline web adapter DI container."""

    # =============================================
    # Calculation conditions adapter
    # ---------------------------------------------
    calculation_conditions = Factory(
        adapters.CalculationConditionsWebAdapter,
    )

    # =============================================
    # Student's exercises (Assigned by mentor)
    # ---------------------------------------------
    student_exercises = Factory(
        adapters.StudentExercisesWebAdapter,
    )

    # =============================================
    # Create calculation case adapter
    # ---------------------------------------------
    create_custom_calculation = Factory(
        adapters.CalculationWebCaseAdapter,
    )
    create_student_calculation = Factory(
        adapters.StudentCalculationWebCaseAdapter,
        domain_adapter=create_custom_calculation,
        # Response may have updated milestone
    )

    # =============================================
    # Explain calculation case adapter
    # ---------------------------------------------
    explain_calculation = Factory(
        adapters.ExplainCalculationWebAdapter,
    )

    # =============================================
    # Adapter strategy
    # ---------------------------------------------
    # for user, include mentor
    custom_calculation_result_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        new_case_adapter=create_custom_calculation,
        explain_adapter=explain_calculation,
    )
    # for student only
    student_calculation_result_strategy = Factory(
        ProcessExerciseAdapterStrategy,
        new_case_adapter=create_student_calculation,
        explain_adapter=explain_calculation,
    )
