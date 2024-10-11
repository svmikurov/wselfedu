"""Foreign app serializers."""

from rest_framework import serializers

from config.constants import (
    FOREIGN_WORD,
    ID,
    RUSSIAN_WORD,
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

    class Meta:
        """Construct serializer."""

        model = TranslateParams
        fields = '__all__'


class WordCategorySerializer(serializers.ModelSerializer):
    """Foreign word Category serializer."""

    class Meta:
        """Setup serializer."""

        model = WordCategory
        fields = '__all__'
