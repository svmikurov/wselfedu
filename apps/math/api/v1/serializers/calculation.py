"""Defines Math app calculation exercise serializers."""

from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.core.types import ResultType
from apps.math.services.types import CalcTaskType

CONFIG_EXAMPLE = {
    'min_value': 1,
    'max_value': 9,
}
CALC_DATA_EXAMPLE = {
    'exercise_name': 'subtraction',
    'config': CONFIG_EXAMPLE,
}

# Task condition serializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid config',
            value=CONFIG_EXAMPLE,
            description='Example of calculation exercise configuration',
        ),
    ],
)
class ConfigSerializer(serializers.Serializer[dict[str, Any]]):
    """Nested serializer for calculation exercise configuration."""

    min_value = serializers.IntegerField()
    max_value = serializers.IntegerField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid calculation data',
            value=CALC_DATA_EXAMPLE,
            description='Example of calculation exercise configuration',
        ),
    ],
)
class ConditionSerializer(serializers.Serializer[dict[str, Any]]):
    """Serializer for calculation condition data.

    Validates and processes the initial data required to perform
    a calculation.
    """

    exercise_name = serializers.CharField(
        max_length=50,
        help_text='Calculation exercise name',
        error_messages={
            'max_length': 'Maximum 50 characters',
        },
    )
    config = ConfigSerializer()


# Serializer to task question


class QuestionSerializer(serializers.Serializer[CalcTaskType]):
    """Serializer for calculation task representation."""

    uid = serializers.UUIDField(
        help_text='Unique identifier of the calculation task'
    )
    question = serializers.CharField(
        max_length=100,
        help_text='String representation of the question',
        error_messages={
            'max_length': 'Maximum 100 characters',
        },
    )


# Serializers for request thr answer check


class AnswerSerializer(serializers.Serializer[dict[str, Any]]):
    """Serializer for calculation task answer."""

    uid = serializers.UUIDField(
        help_text='Unique identifier of the calculation task'
    )
    answer = serializers.CharField(
        max_length=100,
        help_text='String representation of the user answer',
        error_messages={
            'max_length': 'Maximum 100 characters',
        },
    )


class AssignedAnswerSerializer(AnswerSerializer):
    """Serializer for calculation task answer."""

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Add assignation ID to valid data."""
        attrs['assignation_id'] = self.context.get('assignation_id')
        return attrs


# Serializers for task answer result checking


class ResultSerializer(serializers.Serializer[ResultType]):
    """Base serializer for calculation result representation."""

    is_correct = serializers.BooleanField(
        help_text="Is the user's answer correct?",
    )


class ResultAnswerSerializer(ResultSerializer):
    """Serializer for calculation result representation."""

    correct_answer = serializers.CharField(
        max_length=100,
        help_text='String representation of the correct answer',
        error_messages={
            'max_length': 'Maximum 100 characters',
        },
        required=False,
    )
    user_answer = serializers.CharField(
        max_length=100,
        help_text='String representation of the user user answer',
        error_messages={
            'max_length': 'Maximum 100 characters',
        },
        required=False,
    )
