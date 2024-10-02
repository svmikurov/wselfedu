"""Glossary serializer."""

from rest_framework import serializers

from config.constants import (
    CATEGORY,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    PROGRESS,
    USER,
)
from glossary.models import (
    Glossary,
    GlossaryCategory,
    GlossaryParams,
)


class GlossarySerializer(serializers.ModelSerializer):
    """Glossary serializer."""

    class Meta:
        """Construct the serializer."""

        model = Glossary
        fields = '__all__'


class GlossaryParamsSerializer(serializers.ModelSerializer):
    """Glossary Exercise Parameters serializer."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add is created model instance."""
        super().__init__(*args, **kwargs)
        self.is_created = False

    class Meta:
        """Setup serializer."""

        model = GlossaryParams
        fields = [
            PERIOD_START_DATE,
            PERIOD_END_DATE,
            CATEGORY,
            PROGRESS,
        ]

    def create(self, validated_data: dict) -> GlossaryParams:
        """Update or create the user glossary exercise parameters."""
        params, created = GlossaryParams.objects.update_or_create(
            user=validated_data.get(USER),
            defaults=validated_data,
        )
        # HTTP status is 201 if created, otherwise 200.
        if created:
            self.is_created = True
        return params


class GlossaryCategorySerializer(serializers.ModelSerializer):
    """Glossary Category serializer."""

    class Meta:
        """Setup serializer."""

        model = GlossaryCategory
        fields = '__all__'
