"""Glossary exercise view."""

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from config.consts import EDGE_PERIOD_ITEMS, DEFAULT_GLOSSARY_PARAMS
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

    if request.method == 'GET':
        try:
            user_params = GlossaryExerciseParameters.objects.get(user=user)
        except GlossaryExerciseParameters.DoesNotExist:
            parameters = DEFAULT_GLOSSARY_PARAMS
        else:
            serializer = GlossaryExerciseParametersSerializer(user_params)
            parameters = serializer.data

        response_data = {
            'edge_period_items': EDGE_PERIOD_ITEMS,
            'parameters': parameters,
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)
