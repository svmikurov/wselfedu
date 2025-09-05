"""Defines serializers for assigned exercises."""

import logging

from django.db.models import QuerySet
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.study.models import ExerciseAssigned

logger = logging.getLogger(__name__)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Response data',
            value={
                'assignation_id': 3,
                'mentorship_id': 1,
                'mentor_username': 'Dad',
                'exercise_id': 1,
                'exercise_name': 'Multiplication table',
                'count': 20,
                'award': 3,
                'is_active': True,
                'is_daily': True,
                'expiration': '2025-08-12T00:00:00Z',
            },
        )
    ]
)
class AssignedMentorSerializer(
    serializers.Serializer[QuerySet[ExerciseAssigned]]
):
    """Serializer for assigned exercises by mentor."""

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


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Response data',
            value={
                'assignation_id': 2,
                'question_url_path': '/api/v1/math/assigned/2/exercise/division/',  # noqa: E501
                'check_url_path': '/api/v1/math/assigned/2/check/',
                'task_io': 'integer',
            },
            response_only=True,
        )
    ]
)
class SelectExerciseSerializer(serializers.Serializer[ExerciseAssigned]):
    """Serializer for selected exercise configuration."""

    assignation_id = serializers.IntegerField(
        source='id',
        read_only=True,
    )
    question_url_path = serializers.SerializerMethodField()
    check_url_path = serializers.SerializerMethodField()
    task_io = serializers.CharField(
        source='exercise.task_io.alias',
        max_length=100,
    )

    class Meta:
        """Serializer configuration."""

        fields = [
            'assignation_id',
            'question_url_path',
            'check_url_path',
            'task_io',
        ]

    def get_question_url_path(self, obj: ExerciseAssigned) -> str | None:
        """Get exercise URL path."""
        try:
            return reverse(
                f'{obj.exercise.discipline.slug}:assigned_exercise-question',
                kwargs={
                    'exercise_slug': obj.exercise.slug,
                    'assignation_id': obj.pk,
                },
            )

        except NoReverseMatch:
            logger.exception(
                f'URL pattern not found for exercise {obj.exercise}'
            )
            return None

        except AttributeError as e:
            logger.exception(f'Missing attribute for URL generation: {e}')
            return None

    def get_check_url_path(self, obj: ExerciseAssigned) -> str | None:
        """Get URL path to check exercise task user answer."""
        try:
            return reverse(
                f'{obj.exercise.discipline.slug}:assigned_exercise-check',
                kwargs={
                    'assignation_id': obj.pk,
                },
            )

        except NoReverseMatch:
            logger.exception(
                f'URL pattern not found for exercise {obj.exercise}'
            )
            return None

        except AttributeError as e:
            logger.exception(f'Missing attribute for URL generation: {e}')
            return None
