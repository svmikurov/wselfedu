"""Mathematical discipline web adapter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.core.adapter.response.exercise.generic import ResultStrategyAdapter
from apps.math.adapters.response.web import exercise as adapters


class ExerciseWebAdapterContainer(DeclarativeContainer):
    """Mathematical discipline web adapter DI container."""

    # Adapts:
    # - calculation condition form
    calculation_conditions = Factory(
        adapters.CalculationConditionsWebAdapter,
    )
    # Adapts:
    # - current calculation case task data
    create_calculation = Factory(
        adapters.CalculationWebCaseAdapter,
    )
    # Adapts:
    # - current calculation case explanation data
    explain_calculation = Factory(
        adapters.ExplainCalculationWebAdapter,
    )
    # Strategy for user's answer check result
    calculation_result_strategy = Factory(  # type: ignore[var-annotated]
        ResultStrategyAdapter,
        new_case_adapter=create_calculation,
        explain_adapter=explain_calculation,
    )
