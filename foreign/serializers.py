"""Foreign app serializers."""

from django.db.models import Model
from rest_framework import serializers

from config.constants import (
    DEFAULT_LOOKUP_CONDITIONS,
    EDGE_PERIOD_ALIASES,
    NO_SELECTION,
    PROGRESS_ALIASES,
)
from foreign.models import TranslateParams, Word, WordCategory


class WordSerializer(serializers.ModelSerializer):
    """Word serializer."""

    class Meta:
        """Serializer settings."""

        model = Word
        fields = [ID, FOREIGN_WORD, NATIVE_WORD]
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
    """Field alias of pk (`int`).
    """
    humanly = serializers.CharField(source='name')
    """Field alias of name (`str`).
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


class WordAssessmentSerializer(serializers.Serializer):
    """Word knowledge assessment serializer."""

    item_id = serializers.IntegerField()
    """Word ID (`int`).
    """
    action = serializers.CharField(max_length=8)
    """Assessment action (`str`).
    """

    @classmethod
    def validate_item_id(cls, value: int) -> int:
        """Validate the item ID field.

        :param int value: word ID.
        :return int value: word ID.
        :rtype: int
        :raises ValidationError: if word by ID not exists().
        """
        try:
            Word.objects.get(pk=value)
        except Word.DoesNotExist as exc:
            raise serializers.ValidationError(
                f'Слово с ID = {value} не существует'
            ) from exc
        return value

    @classmethod
    def validate_action(cls, value: str) -> str:
        """Validate the action field.

        :param str value: the action alias.
        :return str value: the action alias.
        :rtype: str
        :raises ValidationError: if not correct action alias.
        """
        if value not in ('know', 'not_know'):
            raise serializers.ValidationError(
                'Значение может быть только "know" или "not_know'
            )
        return value

    def validate(self, attrs: dict) -> dict:
        """Check the ownership of the word being assessed.

        :params dict attrs: a dictionary of field values.
        :return attrs: a dictionary of field values.
        :rtype: dict
        :raises ValidationError: if user has not the ownership on the
            word being assessed.
        """
        owner = self.context.get('request').user
        if owner != Word.objects.get(pk=attrs['item_id']).user:
            raise serializers.ValidationError(
                'You can only assessment your own words'
            )
        return attrs
