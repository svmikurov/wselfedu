"""Calculation exercise dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory
from wse_exercises.core.math import RandomOperandGenerator

from apps.math.presenters.assigned import AssignedCalculationPresenter
from apps.math.presenters.calculation import CalculationPresenter
from apps.math.services.calculation import CalcService


class CalculationContainer(DeclarativeContainer):
    """Calculation exercise dependencies container."""

    # -------------------------------------------
    # External dependencies
    # -------------------------------------------

    task_storage = Dependency()  # type: ignore[var-annotated]
    award_service = Dependency()  # type: ignore[var-annotated]
    text_task_checker = Dependency()  # type: ignore[var-annotated]

    # -------------------------------------------
    # Internal dependencies
    # -------------------------------------------

    random_operand_generator = Factory(
        RandomOperandGenerator,
    )
    calculation_exercise_service = Factory(
        CalcService,
        operand_generator=random_operand_generator,
    )

    # -------------------------------------------
    # Calculation exercises
    # -------------------------------------------

    regular_calculation = Factory(
        CalculationPresenter,
        exercise_service=calculation_exercise_service,
        task_storage=task_storage,
        task_checker=text_task_checker,
    )
    # Detail (assigned) calculation exercise
    award_detail_calculation = Factory(
        AssignedCalculationPresenter,
        exercise_service=calculation_exercise_service,
        task_storage=task_storage,
        task_checker=text_task_checker,
        award_service=award_service,
    )
