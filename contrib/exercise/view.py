"""Temporary view of calculation exercise."""

from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from contrib.exercise.base import TaskCreator, AnswerHandler


class ConditionsSerializer(serializers.Serializer):
    """Serializer to get exercise conditions."""

    exercise_type = serializers.CharField(max_length=255)
    min_value = serializers.IntegerField(required=False)
    max_value = serializers.IntegerField(required=False)


class TaskSerializer(serializers.Serializer):
    """Serializer to render task."""
    
    question = serializers.CharField(max_length=255)
    answer = serializers.CharField(max_length=255)


class AnswerSerializer(serializers.Serializer):
    """Serializer to get user answer."""


@api_view(['POST'])
def render_task_view(request: Request) -> Response:
    """Render the task, the view."""
    serializer = ConditionsSerializer(request.data)
    if serializer.is_valid():
        task = TaskCreator(serializer.data, request.user).data
        data = TaskSerializer(task).data
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def handle_answer_view(request: Request) -> Response:
    """Handel the user answer, the view."""
    serializer = AnswerSerializer(request.data)
    if serializer.is_valid():
        AnswerHandler(serializer.data, request.user).handel()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
