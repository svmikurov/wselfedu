"""Mathematical discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Container,
    DependenciesContainer,
    Dependency,
)

from .exercise.calculation import CalculationContainer
from .handler.exercise import ExerciseHandlerContainer
from .view.exercise import ExerciseViewContainer


class MathematicalContainer(DeclarativeContainer):
    """Mathematical discipline DI container."""

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    study_container = DependenciesContainer()

    task_storage = Dependency()  # type: ignore[var-annotated]
    award_service = Dependency()  # type: ignore[var-annotated]

    # -------------------------------------------
    # Internal dependencies
    # -------------------------------------------

    # Temporary exercises container contains only calculation.
    exercises = Container(
        CalculationContainer,
        task_storage=task_storage,
        award_service=award_service,
        text_task_checker=study_container.str_task_checker,
    )
    # Temporary exercises passes to views via handlers without
    # additional functionality.
    handlers = Container(
        ExerciseHandlerContainer,
        exercises=exercises,
    )
    # Views has persistent reference on container dependency.
    exercise_views = Container(
        ExerciseViewContainer,
        handlers=handlers,
        assigned_exercises_selector=study_container.assigned_exercises_selector,
    )
