"""Translate foreign word exercise DRF views."""

import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from config.constants import (
    GET,
    POST,
)
from contrib.views_rest import IsOwner
from foreign.exercise.base import WordAssessment
from foreign.exercise.translate import TranslateExerciseGUI
from foreign.models import TranslateParams
from foreign.serializers import (
    ExerciseChoiceSerializer,
    ExerciseParamSerializer,
    ExerciseSerializer,
    WordAssessmentSerializer,
)


@csrf_exempt
@api_view(['GET', 'PUT'])
@permission_classes((IsOwner,))
def params_view(request: Request) -> JsonResponse | HttpResponse:
    """Render or save the Translate word exercise params.

    **GET method:**
      Render the :term:`exercise_params`.

      Fields:
        - :term:`lookup_conditions`
        - :term:`exercise_choices`

    **PUT method:**
      Save ``lookup_conditions``.
    """
    if request.method == 'GET':
        params, _ = TranslateParams.objects.get_or_create(user=request.user)
        serializer = ExerciseChoiceSerializer(
            params, context={'request': request}
        )
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = ExerciseChoiceSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)

            if serializer.is_created:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view([GET, POST])
@permission_classes((permissions.IsAuthenticated,))
def exercise_view(request: Request) -> JsonResponse | HttpResponse:
    """Render the Translate foreign word exercise the DRF view."""
    # Get exercise parameters.
    params_serializer = ExerciseParamSerializer(data=request.data)
    params_serializer.is_valid()
    # Create exercise task.
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk
    logging.info(f'>>> {lookup_conditions = }')
    exercise_data = TranslateExerciseGUI(lookup_conditions).exercise_data
    # Render the task.
    exercise_serializer = ExerciseSerializer(exercise_data)
    return Response(data=exercise_serializer.data)


@api_view([POST])
@permission_classes((IsOwner,))
def update_word_assessment_view(request: Request) -> Response:
    """Update word study assessment view."""
    serializer = WordAssessmentSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    WordAssessment(request.user, serializer.data).update()
    return Response(status=status.HTTP_204_NO_CONTENT)
