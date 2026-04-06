"""DTO factories."""

from typing import override

from apps.core.factories.abstract import AbstractCaseFactory
from apps.math.domains.dto import (
    CalculationDomainDTO,
    CustomCalculationDTO,
    RegularParametersDTO,
    StudentCalculationDTO,
    StudentParametersDTO,
)


class CustomCalculationDTOFactory(
    AbstractCaseFactory[
        RegularParametersDTO,
        CalculationDomainDTO,
        CustomCalculationDTO,
    ],
):
    """Custom calculation exercise DTO factory."""

    @override
    def build(
        self,
        conf: RegularParametersDTO,
        case: CalculationDomainDTO,
    ) -> CustomCalculationDTO:
        """Create calculation exercise DTO."""
        return CustomCalculationDTO(
            **case.model_dump(),
            **conf.model_dump(),
        )


class StudentCalculationDTOFactory(
    AbstractCaseFactory[
        StudentParametersDTO,
        CalculationDomainDTO,
        StudentCalculationDTO,
    ],
):
    """Student calculation exercise DTO factory."""

    @override
    def build(
        self,
        conf: StudentParametersDTO,
        case: CalculationDomainDTO,
    ) -> StudentCalculationDTO:
        """Create calculation exercise DTO."""
        return StudentCalculationDTO(
            **case.model_dump(),
            **conf.model_dump(),
        )
