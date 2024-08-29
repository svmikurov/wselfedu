"""Project serializers."""

from rest_framework import serializers

from english.models import WordModel


class WordSerializer(serializers.ModelSerializer):
    """Word serializer."""

    class Meta:
        """Construct serializer."""

        model = WordModel
        fields = ['id', 'word_eng', 'word_rus']
