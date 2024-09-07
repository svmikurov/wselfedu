"""Glossary exercise serializer."""

from rest_framework import serializers

from glossary.models import GlossaryExerciseParameters


class GlossaryExerciseParametersSerializer(serializers.ModelSerializer):
    """GlossaryExerciseParameters serializer."""

    class Meta:
        """Setup serializer."""

        model = GlossaryExerciseParameters
        fields = '__all__'
