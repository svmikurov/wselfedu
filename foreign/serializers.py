"""Foreign app serializers."""

from rest_framework import serializers

from config.constants import (
    CATEGORY,
    FOREIGN_WORD,
    ID,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    PROGRESS,
    RUSSIAN_WORD,
    USER,
)
from foreign.models import TranslateParams, Word, WordCategory


class WordSerializer(serializers.ModelSerializer):
    """Word serializer."""

    class Meta:
        """Construct serializer."""

        model = Word
        fields = [ID, FOREIGN_WORD, RUSSIAN_WORD]


class TranslateParamsSerializer(serializers.ModelSerializer):
    """Translate foreign word exercise serializer."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add is created model instance."""
        super().__init__(*args, **kwargs)
        self.is_created = False

    class Meta:
        """Construct serializer."""

        model = TranslateParams
        fields = [
            PERIOD_START_DATE,
            PERIOD_END_DATE,
            CATEGORY,
            PROGRESS,
        ]

    def create(self, validated_data: dict) -> TranslateParams:
        """Update or create the user glossary exercise parameters."""
        params, created = TranslateParams.objects.update_or_create(
            user=validated_data.get(USER),
            defaults=validated_data,
        )
        # HTTP status is 201 if created, otherwise 200.
        if created:
            self.is_created = True
        return params


class WordCategorySerializer(serializers.ModelSerializer):
    """Foreign word Category serializer."""

    class Meta:
        """Setup serializer."""

        model = WordCategory
        fields = '__all__'
