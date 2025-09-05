"""Test Core app index serializer."""

from decimal import Decimal

import pytest

from apps.core.api.v1.serializers.index import IndexSerializer


class TestIndexSerializer:
    """Tests for Core app IndexSerializer."""

    @pytest.mark.parametrize(
        'balance, valid',
        [
            ('123456789.99', False),  # valid max digits and decimal places
            ('0.01', False),
            ('1', True),
            ('12345678901', False),  # too many digits (11 max)
            ('abc', False),  # not a number
            (None, False),  # required field
        ],
    )
    def test_validation_data(
        self,
        balance: str,
        valid: bool,
    ) -> None:
        """Test field validation."""
        data = {
            'balance': balance,
        }
        serializer = IndexSerializer(data=data)

        if valid:
            assert serializer.is_valid()
            assert isinstance(serializer.validated_data['balance'], Decimal)
        else:
            assert not serializer.is_valid()
            assert 'balance' in serializer.errors
