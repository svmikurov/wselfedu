"""Glossary exercise view."""

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from config.constants import (
    CATEGORIES,
    DEFAULT_GLOSSARY_PARAMS,
    EDGE_PERIOD_ALIASES,
    GET,
    POST,
    PROGRES_ALIASES,
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


@api_view([POST])
@permission_classes((permissions.AllowAny,))
def glossary_exercise(request: Request) -> JsonResponse | HttpResponse:
    """Render the Glossary exercise."""
    serializer = GlossaryExerciseParamsSerializer(data=request.data)
    if serializer.is_valid():
        lookup_conditions = serializer.data
        exercise = GlossaryExercise(lookup_conditions).task_data
        return JsonResponse(exercise, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view([GET, POST])
@permission_classes((permissions.AllowAny,))
def glossary_exercise_parameters(
    request: Request,
) -> JsonResponse | HttpResponse:
    """Glossary exercise parameters view.

    GET
    ---
    View sends a response with ``exercise_params``:
        - ``lookup_conditions``
        - ``exercise_choices``

    POST
    ----
    The view updates the ``lookup_conditions`` in data base.

    """
    user = request.user

    if request.method == GET:
        try:
            user_params = GlossaryExerciseParams.objects.get(user=user)
        except GlossaryExerciseParams.DoesNotExist:
            lookup_conditions = DEFAULT_GLOSSARY_PARAMS
        else:
            serializer = GlossaryExerciseParamsSerializer(user_params)
            lookup_conditions = serializer.data

        try:
            user_cats = GlossaryCategory.objects.filter(user=user)
        except GlossaryCategory.DoesNotExist:
            categories = None
        else:
            serializer = GlossaryCategorySerializer(user_cats, many=True)
            categories = serializer.data

        exercise_params = {
            'lookup_conditions': lookup_conditions,
            'exercise_choices': {
                'edge_period_items': EDGE_PERIOD_ALIASES,
                CATEGORIES: categories,
                'progres': PROGRES_ALIASES,
            },
        }

        return JsonResponse(exercise_params, status=HTTP_200_OK)

    if request.method == POST:
        serializer = GlossaryExerciseParamsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if not serializer.is_created:
                return Response(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
