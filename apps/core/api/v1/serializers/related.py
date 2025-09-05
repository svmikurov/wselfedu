"""Related data serializer."""

from apps.users.api.v1.serializers.balance import BalanceSerializer


class RelatedDataSerializer(
    BalanceSerializer,
):
    """Serializer for related data."""
