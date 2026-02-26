"""Mathematical discipline web adapter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.core.adapter.response.exercise.generic import (
    ResultContextStrategyAdapter,
    ResultStrategyAdapter,
)
from apps.math.adapters.response.web import exercise as adapters


class ExerciseWebAdapterContainer(DeclarativeContainer):
    """Mathematical discipline web adapter DI container."""

    # ===========================================
    # Calculation conditions adapter
    # -------------------------------------------
    calculation_conditions = Factory(
        adapters.CalculationConditionsWebAdapter,
    )

    # ===========================================
    # Create calculation case adapter
    # -------------------------------------------
    create_calculation = Factory(
        adapters.CalculationWebCaseAdapter,
    )
    create_student_calculation = Factory(
        adapters.StudentCalculationWebCaseAdapter,
        domain_adapter=create_calculation,
        # Response may have updated milestone
    )

    # ===========================================
    # Explain calculation case adapter
    # -------------------------------------------
    explain_calculation = Factory(
        adapters.ExplainCalculationWebAdapter,
    )

    # ===========================================
    # Adapter strategy
    # -------------------------------------------
    # for user
    calculation_result_strategy = Factory(
        ResultStrategyAdapter,
        new_case_adapter=create_calculation,
        explain_adapter=explain_calculation,
    )
    # for student with balance update
    student_calculation_result_strategy = Factory(
        ResultContextStrategyAdapter,
        new_case_adapter=create_student_calculation,
        explain_adapter=explain_calculation,
    )
