"""Types for project objects."""

from typing import NotRequired, TypedDict

# REVIEW: Update BalanceDataType dependency with generic type?
from apps.users.contracts.general import BalanceDataType


class IndexDataType(TypedDict):
    """Type for index data."""

    status: str
    data: BalanceDataType


class RelatedDataType(BalanceDataType):
    """Type for exercise related data."""


class CheckResultDataType(TypedDict):
    """Type for answer validation result."""

    is_correct: bool
    correct_answer: NotRequired[str]
    user_answer: NotRequired[str]
