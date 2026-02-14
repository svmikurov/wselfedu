"""Mathematical discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.math.use_cases.calculation import (
    CalculationConditionsUseCase,
    RegularCalculationCheckUseCase,
    RegularCalculationCreateUseCase,
)


class ExerciseUseCaseContainer(DeclarativeContainer):
    """Mathematical discipline use case DI container."""

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    services = DependenciesContainer()

    storage = Dependency()  # type: ignore[var-annotated]

    # -------------------------------------------
    # Exercise use cases
    # -------------------------------------------

    calculation_conditions = Factory(
        CalculationConditionsUseCase,
    )

    create_regular_calculation = Factory(
        RegularCalculationCreateUseCase,
        service=services.create_calculation,
        storage=storage,
    )
    check_regular_calculation = Factory(
        RegularCalculationCheckUseCase,
        storage=storage,
        check_service=services.check_calculation,
        milestone_service=services.calculation_milestone,
        create_use_case=create_regular_calculation,
        explain_service=services.explain_calculation,
    )
