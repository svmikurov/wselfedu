"""Mathematical exercise views."""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from contrib.exercise.base import create_task, handel_answer
from contrib.serializers.task import AnswerSerializer, TaskSerializer
from mathematics.serializers.exercise import ConditionsSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def render_task(request: Request) -> Response:
    """Render the task."""
    serializer = ConditionsSerializer(data=request.data)

    if serializer.is_valid():
        task = create_task(serializer.data, request.user)
        task_data = TaskSerializer(task.data_to_render).data
        return Response(task_data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def handle_answer(request: Request) -> Response:
    """Handel the solution."""
    serializer = AnswerSerializer(data=request.data)

    if serializer.is_valid():
        answer = serializer.data
        handel_answer(answer, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
