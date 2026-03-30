"""Mathematical discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.use_cases import null
from apps.math.use_cases import exercises
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
    # Regular calculation exercise conditions select
    calculation_conditions = Factory(
        null.NullUseCase,
    )
    # ---------------------------------------------
    # Regular calculation exercises with temporary
    # exercise parameters passes through request parameters.
    create_regular_calculation = Factory()  # type: ignore
    check_regular_calculation = Factory()  # type: ignore
    # ---------------------------------------------
    # Custom saved calculation exercise requested
    # via the exercise identifier in the request parameters
