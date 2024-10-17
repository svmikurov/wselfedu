"""Foreign app serializers."""

from django.db.models import Model
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
        """Serializer settings."""

        model = Word
        fields = [ID, FOREIGN_WORD, RUSSIAN_WORD]
        """Fields (`list[str]`).
        """


class TranslateParamsSerializer(serializers.ModelSerializer):
    """Translate foreign word exercise serializer."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add is created model instance."""
        super().__init__(*args, **kwargs)
        self.is_created = False

    class Meta:
        """Serializer settings."""

        model = TranslateParams
        fields = [
            PERIOD_START_DATE,
            PERIOD_END_DATE,
            CATEGORY,
            PROGRESS,
        ]
        """Fields (`list[str]`).
        """

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

    alias = serializers.SerializerMethodField()
    """Field alias pk (`int`).
    """
    humanly = serializers.CharField(source='name')
    """Field alias pk (`str`).
    """

    class Meta:
        """Serializer settings."""

        model = WordCategory
        fields = ['alias', 'humanly']
        """Fields (`list[str]`).
        """

    @classmethod
    def get_alias(cls, obj: Model) -> int:
        """Add alias as name of pk field."""
        return obj.pk
