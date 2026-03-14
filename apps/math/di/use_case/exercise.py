"""Mathematical discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.use_cases.exercise import detail, regular
from apps.math.domains.dto_factory import (
    CustomCalculationDTOFactory,
    StudentCalculationDTOFactory,
)
from apps.math.use_cases import calculation, exercises
from apps.study.resolvers.completion import CompletionResolver


class ExerciseUseCaseContainer(DeclarativeContainer):
    """Mathematical discipline use case DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    repositories = DependenciesContainer()
    exercise_services = DependenciesContainer()
    milestone_services = DependenciesContainer()

    storage = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Student's exercises (assigned by mentor)
    # ---------------------------------------------
    student_exercises = Factory(
        exercises.StudentExercisesUseCase,
        resolver=Factory(CompletionResolver),
    )

    # =============================================
    # Exercise use cases
    # ---------------------------------------------
    calculation_conditions = Factory(
        calculation.CalculationConditionsUseCase,
    )

    # ---------------------------------------------
    # Regular calculation exercises with temporary
    # exercise parameters passes through request parameters.
    create_regular_calculation = Factory(
        regular.RegularCreateExerciseUseCase,
        store_prefix='regular_calculation',
        storage=storage,
        service=exercise_services.create_calculation,
    )
    check_regular_calculation = Factory(
        regular.RegularCheckExerciseUseCase,
        store_prefix='regular_calculation',
        storage=storage,
        check_service=exercise_services.check_calculation,
        milestone_service=None,
        create_use_case=create_regular_calculation,
        explain_service=exercise_services.explain_calculation,
    )

    # ---------------------------------------------
    # Custom saved calculation exercise requested
    # via the exercise identifier in the request parameters
    start_custom_calculation = Factory(
        detail.DetailExerciseCreateUseCase,
        store_prefix='custom_calculation',
        storage=storage,
        repository=repositories.calculation_conditions,
        service=exercise_services.create_calculation,
        dto_factory=Factory(CustomCalculationDTOFactory),
    )
    check_custom_calculation = Factory(
        detail.DetailCalculationCheckUseCase,
        store_prefix='custom_calculation',
        storage=storage,
        repository=repositories.calculation_conditions,
        check_service=exercise_services.check_calculation,
        milestone_service=None,
        create_use_case=start_custom_calculation,
        explain_service=exercise_services.explain_calculation,
    )

    # Mentor's exercise handler
    # Start by mentor the exercise assigned to student
    start_mentor_calculation = Factory(
        detail.DetailExerciseCreateUseCase,
        store_prefix='mentor_calculation',
        storage=storage,
        repository=repositories.mentor_calculation_conditions,
        service=exercise_services.create_calculation,
        dto_factory=Factory(CustomCalculationDTOFactory),
    )
    check_mentor_calculation = Factory(
        detail.DetailCalculationCheckUseCase,
        store_prefix='mentor_calculation',
        storage=storage,
        check_service=exercise_services.check_calculation,
        repository=repositories.mentor_calculation_conditions,
        milestone_service=None,
        create_use_case=start_mentor_calculation,
        explain_service=exercise_services.explain_calculation,
    )

    # Student's exercise handler
    start_student_calculation = Factory(
        detail.DetailExerciseCreateUseCase,
        store_prefix='student_calculation',
        storage=storage,
        repository=repositories.student_calculation_conditions,
        service=exercise_services.create_calculation,
        dto_factory=Factory(StudentCalculationDTOFactory),
    )
    check_student_calculation = Factory(
        detail.DetailCalculationCheckUseCase,
        store_prefix='student_calculation',
        storage=storage,
        check_service=exercise_services.check_calculation,
        repository=repositories.student_calculation_conditions,
        milestone_service=milestone_services.student_calculation,
        create_use_case=start_student_calculation,
        explain_service=exercise_services.explain_calculation,
    )
