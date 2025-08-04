"""Defines Math app DI container."""

from dependency_injector import containers, providers
from wse_exercises.core.math import RandomOperandGenerator

from .presenters.calculation import CalcPresenter
from .services.calculation import CalcService


class MathAppContainer(containers.DeclarativeContainer):
    """DI container for Math app components.

    Provides:
        - random_operand_generator: Factory for RandomOperandGenerator
        - calculation_exercise_service: Factory for CalcService
        - calc_presenter: Factory for CalcPresenter
    """

    # External dependencies
    task_storage = providers.Dependency()  # type: ignore[var-annotated]

    # Internal providers
    random_operand_generator = providers.Factory(
        RandomOperandGenerator,
    )

    calculation_exercise_service = providers.Factory(
        CalcService,
        operand_generator=random_operand_generator,
    )

    calc_presenter = providers.Factory(
        CalcPresenter,
        exercise_service=calculation_exercise_service,
        task_storage=task_storage,
    )
