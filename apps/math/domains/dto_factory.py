"""DTO factories."""

from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.math.domains.dto import (
    CalculationDomainDTO,
    CustomCalculationDTO,
    RegularParametersDTO,
    StudentCalculationDTO,
    StudentParametersDTO,
)


class CustomCalculationDTOFactory(
    AbstractExerciseDTOFactory[
        CalculationDomainDTO,
        RegularParametersDTO,
        CustomCalculationDTO,
    ],
):
    """Custom calculation exercise DTO factory."""

    def create(
        self,
        case: CalculationDomainDTO,
        parameters: RegularParametersDTO,
    ) -> CustomCalculationDTO:
        """Create calculation exercise DTO."""
        return CustomCalculationDTO(
            **case.model_dump(),
            **parameters.model_dump(),
        )


class StudentCalculationDTOFactory(
    AbstractExerciseDTOFactory[
        CalculationDomainDTO,
        StudentParametersDTO,
        StudentCalculationDTO,
    ],
):
    """Student calculation exercise DTO factory."""

    def create(
        self,
        case: CalculationDomainDTO,
        parameters: StudentParametersDTO,
    ) -> StudentCalculationDTO:
        """Create calculation exercise DTO."""
        return StudentCalculationDTO(
            **case.model_dump(),
            **parameters.model_dump(),
        )
