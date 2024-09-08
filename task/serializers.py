"""Glossary exercise serializer."""

from rest_framework import serializers

from glossary.models import GlossaryCategory, GlossaryExerciseParams


class GlossaryExerciseParamsSerializer(serializers.ModelSerializer):
    """Glossary Exercise Parameters serializer."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add is created model instance."""
        super().__init__(*args, **kwargs)
        self.is_created = False

    class Meta:
        """Setup serializer."""

        model = GlossaryExerciseParams
        fields = [
            'period_start_date',
            'period_end_date',
            'category',
            'progres',
        ]

    def create(self, validated_data: dict) -> GlossaryExerciseParams:
        """Update or create the user glossary exercise parameters."""
        params, created = GlossaryExerciseParams.objects.update_or_create(
            user=validated_data.get('user'),
            defaults=validated_data,
        )
        if created:
            self.is_created = True
        return params


class GlossaryCategorySerializer(serializers.ModelSerializer):
    """Glossary Category serializer."""

    class Meta:
        """Setup serializer."""

        model = GlossaryCategory
        fields = '__all__'
