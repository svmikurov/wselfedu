"""Mathematical discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.math.use_cases import calculation


class ExerciseUseCaseContainer(DeclarativeContainer):
    """Mathematical discipline use case DI container."""

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    repositories = DependenciesContainer()
    exercise_services = DependenciesContainer()
    milestone_services = DependenciesContainer()

    storage = Dependency()  # type: ignore[var-annotated]

    # -------------------------------------------
    # Exercise use cases
    # -------------------------------------------

    calculation_conditions = Factory(
        calculation.CalculationConditionsUseCase,
    )

    create_regular_calculation = Factory(
        calculation.RegularCalculationCreateUseCase,
        service=exercise_services.create_calculation,
        storage=storage,
    )
    check_regular_calculation = Factory(
        calculation.RegularCalculationCheckUseCase,
        storage=storage,
        check_service=exercise_services.check_calculation,
        milestone_service=None,
        create_use_case=create_regular_calculation,
        explain_service=exercise_services.explain_calculation,
    )

    start_detail_calculation = Factory(
        calculation.DetailCalculationCreateUseCase,
        repository=repositories.calculation_conditions,
        service=exercise_services.create_calculation,
        storage=storage,
    )
    check_detail_calculation = Factory(
        calculation.DetailCalculationCheckUseCase,
        storage=storage,
        check_service=exercise_services.check_calculation,
        milestone_service=milestone_services.user_calculation,
        create_use_case=start_detail_calculation,
        explain_service=exercise_services.explain_calculation,
    )

    start_student_calculation = Factory(
        calculation.DetailCalculationCreateUseCase,
        repository=repositories.student_calculation_conditions,
        service=exercise_services.create_calculation,
        storage=storage,
    )
    check_student_calculation = Factory(
        calculation.DetailCalculationCheckUseCase,
        storage=storage,
        check_service=exercise_services.check_calculation,
        milestone_service=milestone_services.student_calculation,
        create_use_case=start_student_calculation,
        explain_service=exercise_services.explain_calculation,
    )
