"""Mathematical exercise views."""

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from mathematics.exercise.calculation import CalculationExercise
from mathematics.serializers.exercise import MultiplicationSerializer


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def multiplication_exercise_view(request: Request) -> JsonResponse | Response:
    """Multiplication exercise view."""
    # To get task.
    if request.method == 'GET':
        task = CalculationExercise(calculation_type='mul')
        serializer = MultiplicationSerializer(task.data)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)

    # To save answer and points.
    if request.method == 'POST':
        return Response(status=status.HTTP_200_OK)
