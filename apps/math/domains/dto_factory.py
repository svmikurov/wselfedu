"""DTO factories."""

from typing import override

from apps.core.builders.abstract import AbstractCaseFactory
from apps.math.domains.dto import (
    CalculationDomainDTO,
    CustomCalculationDTO,
    StudentCalculationDTO,
)


class CustomCalculationDTOFactory(
    AbstractCaseFactory[
        CalculationDomainDTO,
        CustomCalculationDTO,
    ],
):
    """Custom calculation exercise DTO factory."""

    @override
    def build(
        self,
        option: CalculationDomainDTO,
    ) -> CustomCalculationDTO:
        """Create calculation exercise DTO."""
        return CustomCalculationDTO(
            **option.model_dump(),
        )


class StudentCalculationDTOFactory(
    AbstractCaseFactory[
        CalculationDomainDTO,
        StudentCalculationDTO,
    ],
):
    """Student calculation exercise DTO factory."""

    @override
    def build(
        self,
        option: CalculationDomainDTO,
    ) -> StudentCalculationDTO:
        """Create calculation exercise DTO."""
        return StudentCalculationDTO(
            **option.model_dump(),
        )
