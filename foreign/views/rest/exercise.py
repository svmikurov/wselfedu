"""Translate foreign word exercise DRF views."""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from config.constants import (
    CATEGORIES,
    DEFAULT_LANGUAGE_ORDER,
    DEFAULT_LOOKUP_CONDITIONS,
    DEFAULT_TIMEOUT,
    EDGE_PERIOD_ALIASES,
    EDGE_PERIOD_ITEMS,
    EXERCISE_CHOICES,
    GET,
    LANGUAGE_ORDER,
    LOOKUP_CONDITIONS,
    NO_SELECTION,
    POST,
    PROGRESS,
    PROGRESS_ALIASES,
    TIMEOUT,
    USER_ID,
)
from foreign.exercise.translate import TranslateExerciseGUI
from foreign.models import (
    TranslateParams,
    WordCategory,
)
from foreign.serializers import (
    TranslateParamsSerializer,
    WordCategorySerializer,
)


@csrf_exempt
@api_view([GET, POST])
@permission_classes((permissions.IsAuthenticated,))
def exercise_parameters(request: Request) -> JsonResponse | HttpResponse:
    """Render the Translate word exercise params the DRF view.

    **GET method:**
      Render the :term:`exercise_params`.

      Fields:
        - :term:`lookup_conditions`
        - :term:`exercise_choices`

    **POST method:**
      Save ``lookup_conditions``.
    """
    user = request.user

    if request.method == GET:
        try:
            queryset = TranslateParams.objects.get(user=user)
        except TranslateParams.DoesNotExist:
            lookup_conditions = DEFAULT_LOOKUP_CONDITIONS
        else:
            lookup_conditions = TranslateParamsSerializer(queryset).data

        try:
            queryset = WordCategory.objects.filter(user=user)
        except WordCategory.DoesNotExist:
            queryset = WordCategory.objects.none()
        categories = WordCategorySerializer(queryset, many=True).data
        categories.append(NO_SELECTION)

        exercise_params = {
            LOOKUP_CONDITIONS: lookup_conditions,
            EXERCISE_CHOICES: {
                EDGE_PERIOD_ITEMS: EDGE_PERIOD_ALIASES,
                CATEGORIES: categories,
                PROGRESS: PROGRESS_ALIASES,
            },
        }

        return JsonResponse(exercise_params, status=HTTP_200_OK)

    if request.method == POST:
        serializer = TranslateParamsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if not serializer.is_created:
                return Response(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view([GET, POST])
@permission_classes((permissions.IsAuthenticated,))
def translate_exercise(request: Request) -> JsonResponse | HttpResponse:
    """Render the Translate foreign word exercise the DRF view."""
    serializer = TranslateParamsSerializer(data=request.data)

    if serializer.is_valid():
        lookup_conditions = serializer.data
        lookup_conditions[USER_ID] = request.user.id
        lookup_conditions[TIMEOUT] = DEFAULT_TIMEOUT
        lookup_conditions[LANGUAGE_ORDER] = DEFAULT_LANGUAGE_ORDER

        try:
            exercise = TranslateExerciseGUI(lookup_conditions).task_data
        except IndexError:
            detail = {'detail': 'По заданным условиям задание не сформировано'}
            return JsonResponse(detail, status=HTTP_204_NO_CONTENT)

        return JsonResponse(exercise, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
