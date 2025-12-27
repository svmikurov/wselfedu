"""Presentation schemas."""

from pydantic import BaseModel, ConfigDict, field_validator

from ..types.presentation import TranslationOrder

# ------------------------
# Base presentation models
# ------------------------


class ParametersModel(BaseModel):
    """Provides translation parameters fields."""

    category: int | None = None
    mark: list[int] = []
    source: int | None = None
    start_period: int | None = None
    end_period: int | None = None

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True

    model_config = ConfigDict(
        frozen=True,
    )


class SettingsModel(BaseModel):
    """Provides translation settings fields."""

    translation_order: TranslationOrder = 'to_native'
    word_count: int | None = None

    model_config = ConfigDict(
        frozen=True,
    )


# ------------------------------
# Presentation validation mixins
# ------------------------------


class WebParametersMixin:
    """Provides parameters validation."""

    @field_validator('mark', mode='before')
    @classmethod
    def fix_empty_list(cls, value: str) -> str | list[str]:
        """Fix empty list."""
        return [] if value == '[]' else value

    @field_validator(
        'category', 'source', 'start_period', 'end_period', mode='before'
    )
    @classmethod
    def fix_empty_int(cls, value: str) -> str | None:
        """Return None if string is empty else value."""
        return None if value == '' else value

    @field_validator(
        'is_study', 'is_repeat', 'is_examine', 'is_know', mode='before'
    )
    @classmethod
    def fix_empty_bool(cls, value: str) -> str | bool:
        """Return None if string is empty else value."""
        return True if value == '' else value


class WebSettingsMixin:
    """Provides settings validation."""

    @field_validator('word_count', mode='before')
    @classmethod
    def fix_empty_int(cls, value: str) -> str | None:
        """Return None if string is empty else value."""
        return None if value == '' else value


# ----------------------------
# Request presentation schemas
# ----------------------------


class ParametersSchema(WebParametersMixin, ParametersModel):
    """Presentation parameters schema."""


class SettingsSchema(WebSettingsMixin, SettingsModel):
    """Presentation parameters schema."""


class PresentationRequest(BaseModel):
    """Presentation request."""

    parameters: ParametersModel
    settings: SettingsModel
