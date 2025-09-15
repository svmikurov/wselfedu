"""Defines Core app index serializer."""

from rest_framework import serializers

from apps.core.types import IndexDataType
from apps.users.api.v1.serializers.balance import BalanceSerializer


class IndexSerializer(serializers.Serializer[IndexDataType]):
    """Core app index serializer."""

    status = serializers.ChoiceField(choices=['success', 'error'])
    data = BalanceSerializer()  # type: ignore [assignment]
