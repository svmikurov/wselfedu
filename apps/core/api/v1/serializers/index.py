"""Defines Core app index serializer."""

from rest_framework import serializers

from apps.users.api.v1.serializers.balance import BalanceSerializer
from ports.interfaces.schemas.response.api import IndexDataType


class IndexSerializer(serializers.Serializer[IndexDataType]):
    """Core app index serializer."""

    status = serializers.ChoiceField(choices=['success', 'error'])
    data = BalanceSerializer()  # type: ignore [assignment]
