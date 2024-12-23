"""Glossary serializer."""

from django.db.models import Model
from rest_framework import serializers

from glossary.models import (
    Glossary,
    GlossaryCategory,
    GlossaryParams,
)


class GlossarySerializer(serializers.ModelSerializer):
    """Glossary serializer."""

    class Meta:
        """Serializer settings."""

        model = Glossary
        fields = [
            'term',
            'definition',
        ]


class GlossaryParamsSerializer(serializers.ModelSerializer):
    """Glossary Exercise Parameters serializer."""

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
        """Exclude fields (`list[str]`).
        """

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


class GlossaryCategorySerializer(serializers.ModelSerializer):
    """Glossary Category serializer."""

    alias = serializers.SerializerMethodField()
    """Field alias pk (`int`).
    """
    humanly = serializers.CharField(source='name')
    """Field alias pk (`str`).
    """

    class Meta:
        """Serializer settings."""

        model = GlossaryCategory
        fields = ['alias', 'humanly']
        """Fields (`list[str]`).
        """

    @classmethod
    def get_alias(cls, obj: Model) -> int:
        """Add alias as name of pk field."""
        return obj.pk
