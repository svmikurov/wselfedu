"""Mathematical discipline exercise service DI container."""

from typing import Type

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from wse_exercises.core import math
from wse_exercises.core.math.base.exercise import CalcExercise

from apps.math.domains.enums import CalculationEnum
from apps.math.services import calculation

CALCULATION_DOMAIN_TYPES: dict[CalculationEnum, Type[CalcExercise]] = {
    CalculationEnum.ADD: math.AddingExercise,
    CalculationEnum.SUB: math.SubtractionExercise,
    CalculationEnum.MUL: math.MultiplicationExercise,
    CalculationEnum.DIV: math.DivisionExercise,
}


class ExerciseServiceContainer(DeclarativeContainer):
    """Mathematical discipline exercise service DI container."""

    # -------------------------------------------
    # Calculation exercise
    # -------------------------------------------

    random_operand_generator = Factory(
        math.RandomOperandGenerator,
    )

    create_calculation = Factory(
        calculation.CalculationCreateService,
        domains=CALCULATION_DOMAIN_TYPES,
        operand_generator=random_operand_generator,
    )
    check_calculation = Factory(
        calculation.CalculationCheckService,
    )
    explain_calculation = Factory(
        calculation.CalculationExplainService,
    )
