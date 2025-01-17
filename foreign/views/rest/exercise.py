"""Translate foreign word exercise DRF views."""
import logging
from json import JSONDecoder

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_200_OK,
)

from foreign.queries.lookup_params import WordLookupParams

from config.constants import (
    MSG_NO_TASK,
)
from contrib.views.views_rest import IsOwner
from foreign.exercise.base import WordAssessment
from foreign.exercise.translate import TranslateExerciseGUI
from foreign.models import TranslateParams, Word
from foreign.serializers import (
    ExerciseSerializer,
    ForeignExerciseParamsSerializer,
    WordAssessmentSerializer,
    ForeignParamsSerializer,
    WordSerializer,
)


@csrf_exempt
@api_view(['GET', 'PUT'])
@permission_classes((IsOwner,))
def foreign_params_view(request: Request) -> JsonResponse | HttpResponse:
    """Render or save the Translate word exercise params."""
    user = request.user

    if request.method == 'GET':
        params, _ = TranslateParams.objects.get_or_create(user=user)
        serializer = ForeignParamsSerializer(params, context={'request': request})
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = ForeignParamsSerializer(
            data=request.data, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(user=user)

            if serializer.is_created:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsOwner,))
def foreign_selected_view(request: Request) -> Response:
    """Render the selected words for exercise."""
    # Get exercise parameters.
    params_serializer = ForeignExerciseParamsSerializer(data=request.data)
    params_serializer.is_valid()

    # Create exercise task.
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk

    is_first = lookup_conditions.pop('is_first')
    is_last = lookup_conditions.pop('is_last')
    count_first = lookup_conditions.pop('count_first')
    count_last = lookup_conditions.pop('count_last')

    lookup_params = WordLookupParams(lookup_conditions).params
    queryset = Word.objects.filter(user=request.user, *lookup_params)

    # TODO: Add render items list.
    # TODO: Add filter by first and last.

    return Response(status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsOwner,))
def foreign_exercise_view(request: Request) -> JsonResponse | HttpResponse:
    """Render the Translate foreign word exercise the DRF view."""
    # Get exercise parameters.
    params_serializer = ForeignExerciseParamsSerializer(data=request.data)
    params_serializer.is_valid()

    # Create exercise task.
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk
    try:
        exercise_data = TranslateExerciseGUI(lookup_conditions).exercise_data
    except IndexError:
        data = {'details': MSG_NO_TASK}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    else:
        exercise_serializer = ExerciseSerializer(exercise_data)
        return Response(data=exercise_serializer.data)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_word_assessment_view(request: Request) -> Response:
    """Update word study assessment view."""
    serializer = WordAssessmentSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    WordAssessment(request.user, serializer.data).update()
    return Response(status=status.HTTP_204_NO_CONTENT)
