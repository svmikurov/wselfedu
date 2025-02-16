"""Mathematical exercise views."""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from contrib.exercise.base import TaskCreator, handel_answer
from contrib.serializers.task import AnswerSerializer, TaskSerializer
from mathematics.exercise import EXERCISES
from mathematics.serializers.exercise import (
    ConditionsSerializer,
)
from users.models import UserApp


def get_task(exercise_conditions: dict, user: UserApp) -> TaskCreator:
    """Get task."""
    exercise_type = exercise_conditions.pop('exercise_type')
    exercise_class = EXERCISES[exercise_type]
    exercise = exercise_class(exercise_type)
    task = TaskCreator(exercise, user)
    return task


@api_view(['POST'])
@permission_classes((AllowAny,))
def render_task(request: Request) -> Response:
    """Render the task."""
    serializer = ConditionsSerializer(data=request.data)

    if serializer.is_valid():
        task = get_task(serializer.data, request.user)
        task_data = TaskSerializer(task.data).data
        return Response(task_data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def handle_answer(request: Request) -> Response:
    """Handel the solution."""
    serializer = AnswerSerializer(data=request.data)

    if serializer.is_valid():
        answer = serializer.data
        handel_answer(answer, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
