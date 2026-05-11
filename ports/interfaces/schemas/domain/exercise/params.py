"""Exercise parameters interface."""

from typing import Generic, TypeVar

from pydantic import Field, field_validator

from ports.contract.entity.domain.mixins import (
    WebParametersMixin,
    WebSettingsMixin,
)
from ports.contract.enums.exercise import DisplayOrder
from ports.interfaces.schemas.base import ArbitraryDTO, BaseDTO
from ports.interfaces.schemas.domain.exercise.fields import (
    CaseField,
)

DomainResultT = TypeVar('DomainResultT')

# =================================================
# Lookup conditions
# =================================================


class LookupConditionsDTO(
    WebParametersMixin,
    ArbitraryDTO,
):
    """Provides lookup conditions fields."""

    category: int | None = None
    mark: list[int] = Field(
        default_factory=list,
    )
    source: int | None = None
    start_period: int | None = None
    end_period: int | None = None

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True


# =================================================
# Exercise configuration
# =================================================


# HACK: Split to field composition
class ExerciseConfigDTO(
    WebSettingsMixin,
    BaseDTO,
):
    """Exercise config DTO."""

    display_order: DisplayOrder = Field(
        default=DisplayOrder.DEFINE,
    )
    item_count: int | None = Field(
        description='Candidates of items to exercise count',
        default=None,
    )
    option_count: int | None = Field(
        description='Exercise task option cont (for test exercise)',
        default=7,
    )

    # NOTE: For translation exercise only.
    @field_validator('display_order', mode='before')
    @classmethod
    def normalize_display_order(cls, value: str) -> str:
        """Normalize 'display_order' field."""
        match value:
            case 'to_native':
                return DisplayOrder.MEAN
            case 'from_native':
                return DisplayOrder.DEFINE
            case _:
                return value


# =================================================
# Exercise settings
# =================================================


class ExerciseSettingsDTO(
    BaseDTO,
):
    """Provides translation settings fields."""

    question_timeout: int | None = None
    answer_timeout: int | None = None


# =================================================
# Exercise parameters
# =================================================


class LookupConditionsField(BaseDTO):
    """Lockup conditions DTO field."""

    conditions: LookupConditionsDTO = Field(
        default_factory=LookupConditionsDTO,
    )


class ExerciseConfigField(BaseDTO):
    """Exercise configuration DTO field."""

    conf: ExerciseConfigDTO = Field(
        default_factory=ExerciseConfigDTO,
    )


class ExerciseSettingsField(BaseDTO):
    """Exercise settings DTO field."""

    settings: ExerciseSettingsDTO = Field(
        default_factory=ExerciseSettingsDTO,
    )


class ExerciseParametersDTO(
    LookupConditionsField,
    ExerciseConfigField,
    ExerciseSettingsField,
):
    """Exercise parameters DTO."""


class ExerciseSpecDTO(
    LookupConditionsField,
    ExerciseConfigField,
    ExerciseSettingsField,
    CaseField[DomainResultT],
    Generic[DomainResultT],
):
    """Exercise spec DTO."""


class TestExerciseConfigDTO(
    ExerciseSettingsDTO,
):
    """Provides test exercise configuration DTO."""

    option_count: int
