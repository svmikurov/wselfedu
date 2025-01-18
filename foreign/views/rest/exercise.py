"""Translate foreign word exercise DRF views."""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from config.constants import (
    MSG_NO_TASK,
)
from contrib.views.views_rest import IsOwner
from foreign.exercise.base import WordAssessment
from foreign.exercise.translate import TranslateExerciseGUI
from foreign.models import TranslateParams, Word
from foreign.queries import is_word_in_favorites, update_word_favorites_status
from foreign.queries.lookup_params import WordLookupParams
from foreign.serializers import (
    ExerciseSerializer,
    ForeignExerciseParamsSerializer,
    ForeignParamsSerializer,
    WordAssessmentSerializer,
    WordFavoritesSerilizer,
)


@csrf_exempt
@api_view(['GET', 'PUT'])
@permission_classes((IsOwner,))
def foreign_params_view(request: Request) -> JsonResponse | HttpResponse:
    """Foreign exercise parameters view."""
    user = request.user

    if request.method == 'GET':
        params, _ = TranslateParams.objects.get_or_create(user=user)
        serializer = ForeignParamsSerializer(
            params, context={'request': request}
        )
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = ForeignParamsSerializer(
            data=request.data, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(user=user)

            if serializer.is_created:
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


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

    is_first = lookup_conditions.pop('is_first')  # noqa: F841
    is_last = lookup_conditions.pop('is_last')  # noqa: F841
    count_first = lookup_conditions.pop('count_first')  # noqa: F841
    count_last = lookup_conditions.pop('count_last')  # noqa: F841

    lookup_params = WordLookupParams(lookup_conditions).params
    queryset = Word.objects.filter(*lookup_params, user=request.user)  # noqa: F841

    # TODO: Add render items list.
    # TODO: Add filter by first and last.

    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsOwner,))
def foreign_exercise_view(request: Request) -> JsonResponse | HttpResponse:
    """Foreign exercise view."""
    # Get lookup conditions
    params_serializer = ForeignExerciseParamsSerializer(data=request.data)
    params_serializer.is_valid()
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk

    # Get exercise data
    try:
        exercise_data = TranslateExerciseGUI(lookup_conditions).exercise_data
    except IndexError:
        data = {'details': MSG_NO_TASK}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    # Get favorites status
    is_favorites = is_word_in_favorites(request.user.pk, exercise_data['id'])
    exercise_data['favorites'] = is_favorites

    exercise_serializer = ExerciseSerializer(exercise_data)
    return Response(data=exercise_serializer.data)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_word_progress_view(request: Request) -> Response:
    """Update word study assessment view."""
    serializer = WordAssessmentSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    WordAssessment(request.user, serializer.data).update()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_word_favorites_view(request: Request) -> Response:
    """Update word favorites status view."""
    serializer = WordFavoritesSerilizer(data=request.data)
    serializer.is_valid()

    update_word_favorites_status(
        word_id=serializer.data['id'],
        user_id=request.user.pk,
    )
    return Response(status=status.HTTP_204_NO_CONTENT)
