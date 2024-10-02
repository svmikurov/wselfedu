"""Foreign app serializers."""

from rest_framework import serializers

from config.constants import FOREIGN_WORD, ID, RUSSIAN_WORD
from foreign.models import Word


class WordSerializer(serializers.ModelSerializer):
    """Word serializer."""

    class Meta:
        """Construct serializer."""

        model = Word
        fields = [ID, FOREIGN_WORD, RUSSIAN_WORD]
