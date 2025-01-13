"""Foreign app serializers."""

from typing import Mapping

from rest_framework import serializers

from config.constants import (
    EDGE_PERIOD_CHOICES,
    LANGUAGE_ORDER_CHOICE,
    PROGRESS_CHOICES,
)
from contrib.models.params import DEFAULT_PARAMS
from contrib.views.exercise import create_selection_collection
from foreign.models import TranslateParams, Word, WordCategory, WordSource
from foreign.models.params import DEFAULT_TRANSLATE_PARAMS


class WordSerializer(serializers.ModelSerializer):
    """Word serializer."""

    class Meta:
        """Serializer settings."""

        model = Word
        fields = ['id', 'foreign_word', 'native_word']
        """Fields (`list[str]`).
        """


class ForeignExerciseParamSerializer(serializers.ModelSerializer):
    """Parameters of translate foreign word exercise the serializer."""

    class Meta:
        """Serializer settings."""

        model = TranslateParams
        exclude = ['id', 'user']


class WordParamsSerializer(serializers.ModelSerializer):
    """Choice of translate foreign word params serializer."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add is created model instance."""
        super().__init__(*args, **kwargs)
        self.is_created = False

    class Meta:
        """Serializer settings."""

        model = TranslateParams
        exclude = [
            'id',
            'user',
        ]

    def create(self, validated_data: dict) -> TranslateParams:
        """Update or create the user glossary exercise parameters."""
        params, created = TranslateParams.objects.update_or_create(
            user=validated_data.get('user'),
            defaults=validated_data,
        )
        # HTTP status is 201 if created, otherwise 200.
        if created:
            self.is_created = True
        return params

    def to_internal_value(self, data: Mapping) -> Mapping:
        """Add user ID."""
        internal_data = super().to_internal_value(data)
        user_id = self.context.get('request').user.pk
        internal_data['user_id'] = user_id
        return internal_data

    def to_representation(self, instance: object) -> object:
        """Update the representation data."""
        user = self.context.get('request').user
        lookup_conditions = super().to_representation(instance)

        categories = create_selection_collection(WordCategory, user)
        sources = create_selection_collection(WordSource, user)

        exercise_params = {
            'default_values': DEFAULT_PARAMS | DEFAULT_TRANSLATE_PARAMS,
            'lookup_conditions': lookup_conditions,
            'exercise_choices': {
                'period_start_date': EDGE_PERIOD_CHOICES,
                'period_end_date': EDGE_PERIOD_CHOICES[0:-1],
                'progress': PROGRESS_CHOICES,
                'category': categories,
                'source': sources,
                'order': LANGUAGE_ORDER_CHOICE,
            },
        }

        return exercise_params


class ExerciseSerializer(serializers.Serializer):
    """Foreign exercise serializer."""

    id = serializers.IntegerField()
    question_text = serializers.CharField()
    answer_text = serializers.CharField()
    item_count = serializers.IntegerField()
    assessment = serializers.IntegerField()


class WordCategorySerializer(serializers.ModelSerializer):
    """Foreign word Category serializer."""

    class Meta:
        """Serializer settings."""

        model = WordCategory
        fields = ['id', 'name']


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
