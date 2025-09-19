"""Terms study serializers."""

from rest_framework import serializers

from apps.glossary.types import ParamsType, QuestionType


class TermsStudyParamsSerializer(serializers.Serializer[ParamsType]):
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
    def data(self) -> ParamsType:  # type: ignore[override]
        """Return typed data."""
        return super().data  # type: ignore[return-value]


class TermsStudyQuestionSerializer(serializers.Serializer[QuestionType]):
    """Terms study exercie question serializer."""

    term = serializers.CharField(
        max_length=50,
    )
    definition = serializers.CharField(
        max_length=250,
    )
