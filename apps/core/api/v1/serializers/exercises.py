"""Defines serializers for assigned exercises."""

from rest_framework import serializers

from apps.users.models import ExerciseAssigned


class AssignedMentorSerializer(serializers.Serializer):
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
    expiration = serializers.DateField(read_only=True)

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
