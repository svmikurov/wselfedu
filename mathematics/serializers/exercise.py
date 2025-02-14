"""Mathematics exercises serializers."""

from rest_framework import serializers

from contrib.exercise.base import BaseExercise
from mathematics.exercise import EXERCISES


class CalcSerializer(serializers.Serializer):
    """Multiplication exercise serializer."""

    question = serializers.CharField(max_length=255)
    solution = serializers.CharField(max_length=255)


class ConditionsSerializer(serializers.Serializer):
    """Exercise conditions serializer."""

    exercise_type = serializers.CharField(max_length=255)
    min_value = serializers.IntegerField(required=False)
    max_value = serializers.IntegerField(required=False)

    @classmethod
    def validate_exercise_type(cls, exercise: BaseExercise) -> BaseExercise:
        """Validate if exercise type exists."""
        if exercise not in EXERCISES:
            raise serializers.ValidationError(
                f'Exercise {exercise} not exists'
            )
        return exercise
