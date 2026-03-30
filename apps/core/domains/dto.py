"""Base Data Transfer Object."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

# =================================================
# DTO configuration mixins
# =================================================


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


class ProtectDefaultStatusMixin:
    """Ensures status uses default value."""

    @model_validator(mode='before')
    @classmethod
    def remove_status_if_passed(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Remove status field to assign the default value."""
        if isinstance(data, dict):
            data.pop('status', None)
        return data


# =================================================
# Base DTOs
# =================================================


class BaseDTO(BaseConfigurationMixin, BaseModel):
    """Base Data Transfer Objects model."""


class ArbitraryDTO(ArbitraryConfigurationMixin, BaseModel):
    """Base Data Transfer Objects model with arbitrary types."""


# =================================================
# DTO fields
# =================================================


class ErrorField(BaseDTO):
    """Error message DTO field."""

    error_message: str = Field(
        description='Error message',
    )
