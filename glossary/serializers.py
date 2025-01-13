"""Term serializer."""

from typing import Mapping

from django.db.models import Model
from rest_framework import serializers

from config.constants import EDGE_PERIOD_CHOICES, PROGRESS_CHOICES
from contrib.models.params import DEFAULT_PARAMS
from contrib.views.exercise import create_selection_collection
from glossary.models import (
    GlossaryParams,
    Term,
    TermCategory,
    TermSource,
)

DEFAULT_GLOSSARY_PARAMS = {
    'category': None,
    'source': None,
}


class TermSerializer(serializers.ModelSerializer):
    """Term serializer."""

    class Meta:
        """Serializer settings."""

        model = Term
        fields = [
            'id',
            'term',
            'definition',
        ]


class GlossaryExerciseParamSerializer(serializers.ModelSerializer):
    """Parameters of translate foreign word exercise the serializer."""

    class Meta:
        """Serializer settings."""

        model = GlossaryParams
        exclude = ['id', 'user']


class TermParamsSerializer(serializers.ModelSerializer):
    """Term Exercise Parameters serializer."""

    no_selection = [None, 'Не выбрано']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add is created model instance."""
        super().__init__(*args, **kwargs)
        self.is_created = False

    class Meta:
        """Serializer settings."""

        model = GlossaryParams
        exclude = [
            'id',
            'user',
        ]

    def create(self, validated_data: dict) -> GlossaryParams:
        """Update or create the user glossary exercise parameters."""
        params, created = GlossaryParams.objects.update_or_create(
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

        categories = create_selection_collection(TermCategory, user)
        sources = create_selection_collection(TermSource, user)

        exercise_params = {
            'default_values': DEFAULT_PARAMS | DEFAULT_GLOSSARY_PARAMS,
            'lookup_conditions': lookup_conditions,
            'exercise_choices': {
                'period_start_date': EDGE_PERIOD_CHOICES,
                'period_end_date': EDGE_PERIOD_CHOICES[0:-1],
                'progress': PROGRESS_CHOICES,
                'category': categories,
                'source': sources,
            },
        }

        return exercise_params


class TermCategorySerializer(serializers.ModelSerializer):
    """Term Category serializer."""

    alias = serializers.SerializerMethodField()
    """Field alias pk (`int`).
    """
    humanly = serializers.CharField(source='name')
    """Field alias pk (`str`).
    """

    class Meta:
        """Serializer settings."""

        model = TermCategory
        fields = ['alias', 'humanly']
        """Fields (`list[str]`).
        """

    @classmethod
    def get_alias(cls, obj: Model) -> int:
        """Add alias as name of pk field."""
        return obj.pk
