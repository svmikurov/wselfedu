"""Test the preparation of data for Core app index view."""

from decimal import Decimal
from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser

from apps.core.presenters.index import get_index_data


def test_for_authenticated_user() -> None:
    """Test the preparation of data for authenticated user."""
    user = Mock(
        is_authenticated=True,
        balance_total=33,
    )
    assert get_index_data(user) == {
        'balance': Decimal(33),
    }


def test_for_anonymous_user() -> None:
    """Test the preparation of data for anonymous user."""
    user = AnonymousUser()
    assert get_index_data(user) == {
        'balance': None,
    }
