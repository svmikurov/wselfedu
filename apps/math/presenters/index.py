"""Prepare Math app data for index views DRF."""

from typing import Any

from django.contrib.auth.models import AnonymousUser

from apps.users.models import Person


def get_index_data(
    user: Person | AnonymousUser,
) -> dict[str, Any]:
    """Aggregate Math app data for API response.

    Args:
        user: User instance (authenticated or anonymous)

    Returns:
        Dict with:
            - user_balance: float | None
            - exercises: list[str]

    """
    if user.is_authenticated:
        return {
            'balance': user.balance_total,
            'exercises': [
                'Adding',
                'Multiplication',
            ],
        }
    else:
        return {
            'balance': None,
            'exercises': [
                'Adding',
                'Multiplication',
            ],
        }
