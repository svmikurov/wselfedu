"""Glossary exercise view."""

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from glossary.models import GlossaryExerciseParameters
from task.serializers import GlossaryExerciseParametersSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def glossary_exercise(request: Request) -> Response:
    """Render the Glossary exercise."""
    data = {'status': 'ok'}
    return Response(
        data=data,
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def glossary_exercise_parameters(
    request: Request,
) -> JsonResponse | HttpResponse:
    """Glossary exercise api view."""
    user = request.user
    try:
        parameters = GlossaryExerciseParameters.objects.get(user=user)
    except GlossaryExerciseParameters.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GlossaryExerciseParametersSerializer(parameters)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
