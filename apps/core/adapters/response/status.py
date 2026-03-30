"""Response status enumeration."""

from apps.core.enums import BaseEnum


class StatusEnum(BaseEnum):
    """Response status enumeration."""

    OK = 'ok'
    NEW_CASE = 'new_case'
    EXPLAIN = 'correct and wrong answer explanation'
