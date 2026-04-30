"""Response status enumeration."""

from contracts.enums.base import BaseEnum


class ResponseStatusEnum(BaseEnum):
    """Response status enumeration."""

    OK = 'ok'
    NEW_CASE = 'new_case'
    EXPLAIN_CASE = 'explain_case'
    NO_CASE = 'no_case'
