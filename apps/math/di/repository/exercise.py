"""Mathematical discipline exercise web repositories."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.math.models import (
    AssignedCalculationCondition,
    CalculationCondition,
)
from apps.math.repositories.exercise import (
    CalculationConditionsRepository,
    StudentCalculationConditionsRepository,
)


class ExerciseRepositoryContainer(DeclarativeContainer):
    """Mathematical discipline exercise web repositories."""

    calculation_conditions = Factory(
        CalculationConditionsRepository,
        manager=CalculationCondition.objects,
    )
    student_calculation_conditions = Factory(
        StudentCalculationConditionsRepository,
        manager=AssignedCalculationCondition.objects,
    )
