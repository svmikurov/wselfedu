"""Defines serializers for assigned exercises."""

from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.users.models import ExerciseAssigned


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Response data',
            value={
                'assignation_id': 3,
                'mentorship_id': 1,
                'mentor_username': "Папа",
                'exercise_id': 1,
                'exercise_name': 'Таблица умножения',
                'count': 20,
                'award': 3,
                'is_active': True,
                'is_daily': True,
                'expiration': '2025-08-12T00:00:00Z',
            },
            response_only=True,
        )
    ]
)
class AssignedMentorSerializer(
    serializers.Serializer[QuerySet[ExerciseAssigned]]
):
    """Serializer for assigned exercises by one mentor."""

    assignation_id = serializers.IntegerField(
        source='pk',
        read_only=True,
    )
    mentorship_id = serializers.IntegerField(
        source='mentorship.id',
        read_only=True,
    )
    mentor_username = serializers.CharField(
        source='mentorship.mentor',
        max_length=150,
    )
    exercise_id = serializers.IntegerField(
        source='exercise.id',
        read_only=True,
    )
    exercise_name = serializers.CharField(
        source='exercise.name',
        read_only=True,
    )
    count = serializers.IntegerField(
        read_only=True,
    )
    award = serializers.IntegerField(
        read_only=True,
    )
    is_active = serializers.BooleanField(
        read_only=True,
    )
    is_daily = serializers.BooleanField(
        read_only=True,
    )
    expiration = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        """Serializer configration."""

        model = ExerciseAssigned
        fields = [
            'assignation_id',
            'mentorship_id',
            'mentor_username',
            'exercise_id',
            'exercise_name',
            'count',
            'award',
            'is_active',
            'is_daily',
            'expiration',
        ]
