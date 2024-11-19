"""Term serializer."""

from django.db.models import Model
from rest_framework import serializers

from glossary.models import (
    GlossaryParams,
    Term,
    TermCategory,
)


class TermSerializer(serializers.ModelSerializer):
    """Term serializer."""

    class Meta:
        """Serializer settings."""

        model = Term
        fields = [
            'term',
            'definition',
        ]


class TermParamsSerializer(serializers.ModelSerializer):
    """Term Exercise Parameters serializer."""

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
