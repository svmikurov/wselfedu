"""Terms study serializers."""

from rest_framework import serializers

from apps.glossary.types import TermParamsType, TermType


class TermStudyParamsSerializer(serializers.Serializer[TermParamsType]):
    """Terms study exercie parameters of request serializer."""

    category = serializers.ListField(
        child=serializers.CharField(
            max_length=50,
        ),
    )
    marks = serializers.ListField(
        child=serializers.CharField(
            max_length=50,
        ),
        required=False,
    )

    @property
    def data(self) -> TermParamsType:  # type: ignore[override]
        """Return typed data."""
        return super().data  # type: ignore[return-value]


class TermStudyPresentationSerializer(serializers.Serializer[TermType]):
    """Terms study exercie question serializer."""

    term = serializers.CharField(
        max_length=50,
    )
    definition = serializers.CharField(
        max_length=250,
    )
