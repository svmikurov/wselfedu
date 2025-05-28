"""Defines math app DI container."""

from dependency_injector import containers, providers
from wse_exercises import (
    DivisionExercise,
    MultiplicationExercise,
    SubtractionExercise,
)
from wse_exercises.core.mathem import (
    AddingExercise,
    RandomOperandGenerator,
)

from services.exercise import SimpleMathExerciseService

from .constants import MATH_EXERCISE_CONFIG_PATH


class MathExercisesContainer(containers.DeclarativeContainer):
    """DI container for math exercises."""

    # Container dependencies
    math_container = providers.DependenciesContainer()

    # Exercise configurations
    simple_exercise_config = math_container.config.provided['simple_exercise']

    # Exercise providers
    adding = providers.Factory(
        AddingExercise,
        operand_generator=math_container.random_operand_generator,
        config=simple_exercise_config,
    )
    division = providers.Factory(
        DivisionExercise,
        operand_generator=math_container.random_operand_generator,
        config=simple_exercise_config,
    )
    multiplication = providers.Factory(
        MultiplicationExercise,
        operand_generator=math_container.random_operand_generator,
        config=simple_exercise_config,
    )
    subtraction = providers.Factory(
        SubtractionExercise,
        operand_generator=math_container.random_operand_generator,
        config=simple_exercise_config,
    )


class MathContainer(containers.DeclarativeContainer):
    """DI container for math exercises."""

    wiring_config = containers.WiringConfiguration(
        modules=['apps.mathem.api.v1.views']
    )

    # Configuration
    config = providers.Configuration()
    config.from_yaml(MATH_EXERCISE_CONFIG_PATH)

    # Component providers
    random_operand_generator = providers.Singleton(
        RandomOperandGenerator,
    )

    # Exercises container
    exercises_container = providers.Container(
        MathExercisesContainer,
        math_container=providers.DependenciesContainer(
            random_operand_generator=random_operand_generator,
            config=config,
        ),
    )

    # Exercise services
    exercise_service = providers.Factory(
        SimpleMathExerciseService,
        exercises_container=exercises_container,
    )
