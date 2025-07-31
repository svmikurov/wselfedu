"""Prepare data for index views DRF."""

from typing import Any

from django.contrib.auth.models import AnonymousUser

from apps.users.models import CustomUser


def get_index_data(
    user: CustomUser | AnonymousUser,
) -> dict[str, Any]:
    """Get common index response data."""
    if user.is_authenticated:
        return {
            'balance': user.balance_total,
        }
    else:
        return {}
