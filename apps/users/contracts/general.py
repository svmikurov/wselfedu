"""Users application contracts."""

from decimal import Decimal
from typing import TypedDict


class BalanceDataType(TypedDict):
    """Type for balance data."""

    balance: Decimal | None
