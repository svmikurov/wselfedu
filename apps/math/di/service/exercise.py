"""Mathematical exercise services DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from wse_exercises.core import math

from apps.math.domains.enums import CalculationEnum
from apps.math.services import calculation

CALCULATION_DOMAIN_TYPES = {
    CalculationEnum.ADD: math.AddingExercise,
    CalculationEnum.SUB: math.SubtractionExercise,
    CalculationEnum.MUL: math.MultiplicationExercise,
    CalculationEnum.DIV: math.DivisionExercise,
}


class ExerciseServiceContainer(DeclarativeContainer):
    """Mathematical exercise services DI container."""

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
