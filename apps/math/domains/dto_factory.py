"""DTO factories."""

from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.math.domains.dto import (
    CalculationDomainDTO,
    CalculationDTO,
    StudentParametersDTO,
)


class CalculationDTOFactory(
    AbstractExerciseDTOFactory[
        CalculationDomainDTO,
        StudentParametersDTO,
        CalculationDTO,
    ],
):
    """Calculation exercise DTO factory."""

    def create(
        self,
        case: CalculationDomainDTO,
        parameters: StudentParametersDTO,
    ) -> CalculationDTO:
        """Create calculation exercise DTO."""
        return CalculationDTO(**case.model_dump(), **parameters.model_dump())
