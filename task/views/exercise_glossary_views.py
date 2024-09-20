"""Glossary exercise view."""

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from config.consts import (
    CATEGORIES,
    DEFAULT_GLOSSARY_PARAMS,
    EDGE_PERIOD_ITEMS,
    GET,
    POST,
    PROGRES_STAGES,
)
from glossary.models import (
    GlossaryCategory,
    GlossaryExerciseParams,
)
from task.serializers import (
    GlossaryCategorySerializer,
    GlossaryExerciseParamsSerializer,
)
from task.tasks.glossary_exercise import GlossaryExercise


@api_view([GET])
@permission_classes((permissions.AllowAny,))
def glossary_exercise(request: Request) -> JsonResponse | HttpResponse:
    """Render the Glossary exercise."""
    query = GlossaryExerciseParams.objects.get(user=request.user)
    exercise_params = model_to_dict(query)
    task_data = GlossaryExercise(exercise_params).task_data
    return JsonResponse(task_data, status=status.HTTP_200_OK)


@api_view([GET, POST])
@permission_classes((permissions.AllowAny,))
def glossary_exercise_parameters(
    request: Request,
) -> JsonResponse | HttpResponse:
    """Glossary exercise api view."""
    user = request.user

    if request.method == GET:
        try:
            user_params = GlossaryExerciseParams.objects.get(user=user)
        except GlossaryExerciseParams.DoesNotExist:
            parameters = DEFAULT_GLOSSARY_PARAMS
        else:
            serializer = GlossaryExerciseParamsSerializer(user_params)
            parameters = serializer.data

        try:
            user_cats = GlossaryCategory.objects.filter(user=user)
        except GlossaryCategory.DoesNotExist:
            categories = None
        else:
            serializer = GlossaryCategorySerializer(user_cats, many=True)
            categories = serializer.data

        response_data = {
            'edge_period_items': EDGE_PERIOD_ITEMS,
            CATEGORIES: categories,
            'parameters': parameters,
            'progres': PROGRES_STAGES,
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)

    if request.method == POST:
        serializer = GlossaryExerciseParamsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if not serializer.is_created:
                return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
