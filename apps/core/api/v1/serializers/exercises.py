"""Defines serializers for assigned exercises."""

from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.users.models import ExerciseAssigned


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid data',
            value={
                'mentorship_id': 1,
                'exercise_id': 1,
                'exercise_name': 'Таблица умножения',
                'count': 20,
                'award': 3,
                'is_active': True,
                'is_daily': True,
                'expiration': '2025-08-12T00:00:00Z',
            },
            description='Example of assigned exercise',
        )
    ]
)
class AssignedMentorSerializer(
    serializers.Serializer[QuerySet[ExerciseAssigned]]
):
    """Serializer for assigned exercises by one mentor."""

    mentorship_id = serializers.IntegerField(
        source='mentorship.id', read_only=True
    )
    exercise_id = serializers.IntegerField(
        source='exercise.id', read_only=True
    )
    exercise_name = serializers.CharField(
        source='exercise.name', read_only=True
    )
    count = serializers.IntegerField(read_only=True)
    award = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_daily = serializers.BooleanField(read_only=True)
    expiration = serializers.DateTimeField(read_only=True)

    class Meta:
        """Serializer configration."""

        model = ExerciseAssigned
        fields = [
            'id',
            'mentorship_id',
            'exercise_id',
            'exercise_name',
            'count',
            'award',
            'is_active',
            'is_daily',
            'expiration',
        ]
