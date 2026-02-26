"""Base Data Transfer Object."""

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BaseConfigurationMixin:
    """Provides base configuration for Data Transfer Objects."""

    model_config = ConfigDict(
        extra='forbid',
        frozen=True,
    )


class BaseDTO(BaseConfigurationMixin, BaseModel):
    """Base Data Transfer Objects model."""


class ProtectDefaultStatusMixin:
    """Ensures status uses default value."""

    @model_validator(mode='before')
    @classmethod
    def remove_status_if_passed(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Remove status field to assign the default value."""
        if isinstance(data, dict):
            data.pop('status', None)
        return data
