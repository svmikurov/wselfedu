"""Defines Math app calculation exercise serializers."""

from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

# TODO: Add other examples

# TODO:
# ConfigData(BaseModel):
# min_value: int
# max_value: int
#
# OpenApiExample(
#   'Valid config',
#   value=TypeData(ConfigData),

# Nested schemas

CONFIG_EXAMPLE = {
    'min_value': 1,
    'max_value': 9,
}

# Request schemas

CALC_DATA_EXAMPLE = {
    'exercise_name': 'subtraction',
    'config': CONFIG_EXAMPLE,
}

# Response schemas

...


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid config',
            value=CONFIG_EXAMPLE,
            description='Example of calculation exercise configuration',
        ),
    ],
)
class CalcConfSerializer(serializers.Serializer[dict[str, Any]]):
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
class CalcDataSerializer(serializers.Serializer[dict[str, Any]]):
    """Serializer for calculation input data.

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
    config = CalcConfSerializer()


class CalcTaskSerializer(serializers.Serializer[dict[str, Any]]):
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


class CalcAnswerSerializer(serializers.Serializer[dict[str, Any]]):
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


class CalcResultSerializer(serializers.Serializer[dict[str, Any]]):
    """Serializer for calculation result representation."""

    is_correct = serializers.BooleanField(
        help_text="Is the user's answer correct?",
    )
    correct_answer = serializers.CharField(
        max_length=100,
        help_text='String representation of the correct answer',
        error_messages={
            'max_length': 'Maximum 100 characters',
        },
    )
