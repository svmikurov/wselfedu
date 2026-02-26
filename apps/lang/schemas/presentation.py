"""Presentation schemas."""

from pydantic import BaseModel, ConfigDict, field_validator

from apps.core.domains.exercise import DisplayOrder

# ------------------------
# Base presentation models
# ------------------------

# REVIEW: Now schemas include translation order,
# it limits the use of the scheme in other exercises.


class LookupCondition(BaseModel):
    """Provides lookup conditions fields."""

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

    display_order: DisplayOrder = DisplayOrder.DEFINE
    item_count: int | None = None

    model_config = ConfigDict(
        frozen=True,
    )

    @field_validator('display_order', mode='before')
    @classmethod
    def normalize_display_order(cls, value: str) -> str:
        """Normalize 'display_order' field."""
        match value:
            case 'to_native':
                return DisplayOrder.EXPLAIN
            case 'from_native':
                return DisplayOrder.DEFINE
            case _:
                return value


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

    @field_validator('item_count', mode='before')
    @classmethod
    def fix_empty_int(cls, value: str) -> str | None:
        """Return None if string is empty else value."""
        return None if value == '' else value


# ----------------------------
# Request presentation schemas
# ----------------------------


class ParametersSchema(WebParametersMixin, LookupCondition):
    """Presentation parameters schema."""


class SettingsSchema(WebSettingsMixin, SettingsModel):
    """Presentation parameters schema."""


class RegularConditionRequest(BaseModel):
    """Regular request with study conditions."""

    parameters: LookupCondition
    settings: SettingsModel
