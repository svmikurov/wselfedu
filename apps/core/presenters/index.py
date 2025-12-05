"""Prepare Core app data for index views DRF."""

from django.contrib.auth.models import AnonymousUser

from apps.core.types import BalanceDataType
from apps.users.models import Person


def get_index_data(
    user: Person | AnonymousUser,
) -> BalanceDataType:
    """Aggregate Core app data for API response.

    Args:
        user: User instance (authenticated or anonymous)

    Returns:
        Dict with:
            - user_balance: float | None

    """
    if user.is_authenticated:
        return {
            'balance': user.balance_total,
        }
    else:
        return {
            'balance': None,
        }
