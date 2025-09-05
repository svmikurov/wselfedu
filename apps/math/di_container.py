"""Defines Math app DI container."""

from dependency_injector import containers, providers
from wse_exercises.core.math import RandomOperandGenerator

from ..study.servises.checker import StrTaskChecker
from .presenters.calculation import CalculationPresenter
from .services.calculation import CalcService


class MathAppContainer(containers.DeclarativeContainer):
    """DI container for Math app dependencies."""

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
    str_task_checker = providers.Factory(
        StrTaskChecker,
    )

    calc_presenter = providers.Factory(
        CalculationPresenter,
        exercise_service=calculation_exercise_service,
        task_storage=task_storage,
        task_checker=str_task_checker,
    )
