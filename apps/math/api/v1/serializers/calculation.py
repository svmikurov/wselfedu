"""Defines Math app calculation exercise serializers."""

from typing import Any

from rest_framework import serializers


class CalcConfSerializer(serializers.Serializer[dict[str, Any]]):
    """Serializer for calculation exercise configuration."""

    min_value = serializers.IntegerField()
    max_value = serializers.IntegerField()


class CalcDataSerializer(serializers.Serializer[dict[str, Any]]):
    """Serializer for calculation input data.

    Validates and processes the initial data required to perform
    a calculation.

    Fields:
        exercise (str): Calculation exercise name
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
    """Serializer for calculation task representation.

    Contains complete information about a calculation task including:
        uid (UUID): Unique identifier of the calculation task,
        task (str): String representation of the task
    """

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
