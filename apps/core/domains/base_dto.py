"""Base Data Transfer Object."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BaseConfigurationMixin:
    """Provides base configuration for Data Transfer Objects."""

    model_config = ConfigDict(
        extra='forbid',
        frozen=True,
    )


class ArbitraryConfigurationMixin:
    """Provides arbitrary configuration for Data Transfer Objects."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class BaseDTO(BaseConfigurationMixin, BaseModel):
    """Base Data Transfer Objects model."""


class ArbitraryDTO(ArbitraryConfigurationMixin, BaseModel):
    """Base Data Transfer Objects model with arbitrary types."""


class ProtectDefaultStatusMixin:
    """Ensures status uses default value."""

    @model_validator(mode='before')
    @classmethod
    def remove_status_if_passed(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Remove status field to assign the default value."""
        if isinstance(data, dict):
            data.pop('status', None)
        return data


class UuidDTO(BaseDTO):
    """Stored exercise case UUID DTO."""

    case_uuid: UUID = Field(
        description='Stored exercise case UUID',
    )
