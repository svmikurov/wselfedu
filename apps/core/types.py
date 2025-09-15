"""Types for project objects."""

from decimal import Decimal
from typing import NotRequired, TypedDict


class BalanceDataType(TypedDict):
    """Type for balance data."""

    balance: Decimal | None


class IndexDataType(TypedDict):
    """Type for index data."""

    status: str
    data: BalanceDataType


class RelatedDataType(BalanceDataType):
    """Type for exercise related data."""


class ResultType(TypedDict):
    """Type for answer validation result."""

    is_correct: bool
    correct_answer: NotRequired[str]
    user_answer: NotRequired[str]
