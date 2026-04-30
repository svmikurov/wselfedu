"""Domain DTO's mixins."""

from pydantic import field_validator


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
