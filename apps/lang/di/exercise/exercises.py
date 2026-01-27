"""Language discipline Exercises DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Container,
    DependenciesContainer,
    Dependency,
)

from .presentation import PresentationContainer
from .test import TranslationTestContainer


class ExercisesContainer(DeclarativeContainer):
    """Language discipline Exercises DI container.

    Provides the exercise routes.
    """

    # ---------------------
    # External dependencies
    # ---------------------

    adapters = DependenciesContainer()
    exercise_case_storage = Dependency()  # type: ignore[var-annotated]

    # ------------------------------------------
    # Translation Presentation exercise UseCases
    # ------------------------------------------

    presentation_exercises = Container(
        PresentationContainer,
        task_storage=exercise_case_storage,
    )
    web_presentation = presentation_exercises.web_use_case
    api_presentation = presentation_exercises.api_use_case

    # ----------------------------------
    # Translation Test exercise UseCases
    # ----------------------------------

    test_exercises = Container(
        TranslationTestContainer,
        task_storage=exercise_case_storage,
        web_adapter=adapters.web_test,
    )

    web_test = test_exercises.web_regular_use_case
    web_test_progress = test_exercises.web_progress_use_case
    web_test_mentorship = test_exercises.web_assigned_use_case
