"""Project serializers."""

from rest_framework import serializers

from config.constants import FOREIGN_WORD, ID, RUSSIAN_WORD
from english.models import WordModel


class WordSerializer(serializers.ModelSerializer):
    """Word serializer."""

    class Meta:
        """Construct serializer."""

        model = WordModel
        fields = [ID, FOREIGN_WORD, RUSSIAN_WORD]
