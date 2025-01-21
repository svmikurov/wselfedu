"""Translate foreign word exercise DRF views."""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from config.constants import MSG_NO_TASK
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
    WordFavoritesSerializer,
    WordSerializer,
)


@api_view(['GET', 'PUT'])
@permission_classes((IsOwner,))
def foreign_params_view(request: Request) -> JsonResponse | HttpResponse:
    """Foreign exercise parameters view."""
    context = {'request': request}

    if request.method == 'GET':
        params, _ = TranslateParams.objects.get_or_create(user=request.user)
        serializer = ForeignParamsSerializer(params, context=context)
        return JsonResponse(serializer.data, status=HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data
        serializer = ForeignParamsSerializer(data=data, context=context)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if serializer.is_created:
                return JsonResponse(serializer.data, status=HTTP_201_CREATED)
            return HttpResponse(status=HTTP_204_NO_CONTENT)

        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsOwner,))
def foreign_selected_view(request: Request) -> JsonResponse:
    """Render the selected words for exercise."""
    request_serializer = ForeignExerciseParamsSerializer(data=request.data)
    request_serializer.is_valid()
    lookup_conditions = request_serializer.data
    lookup_conditions['user_id'] = request.user.pk

    is_first = lookup_conditions.pop('is_first')
    is_last = lookup_conditions.pop('is_last')
    count_first = lookup_conditions.pop('count_first')
    count_last = lookup_conditions.pop('count_last')

    lookup_params = WordLookupParams(lookup_conditions).params
    queryset = Word.objects.filter(*lookup_params, user=request.user)

    if is_first and is_last:
        queryset_first = queryset[:count_first]
        queryset_last = queryset.order_by('-pk')[:count_last]
        queryset = queryset_last.union(queryset_first).order_by('pk')
    elif is_first:
        queryset = queryset[:count_first]
    elif is_last:
        queryset = queryset.order_by('-pk')[:count_last]

    paginator = PageNumberPagination()
    paginator.page_size = 20
    result = paginator.paginate_queryset(queryset, request)
    serializer = WordSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsOwner,))
def foreign_exercise_view(request: Request) -> JsonResponse:
    """Foreign exercise view."""
    # Get lookup conditions
    params_serializer = ForeignExerciseParamsSerializer(data=request.data)
    params_serializer.is_valid()
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk

    # Get exercise data
    try:
        exercise_data = TranslateExerciseGUI(lookup_conditions).task_data
    except IndexError:
        details = {'details': MSG_NO_TASK}
        return JsonResponse(details, status=HTTP_204_NO_CONTENT)

    # Get favorites status
    is_favorites = is_word_in_favorites(request.user.pk, exercise_data['id'])
    exercise_data['favorites'] = is_favorites

    exercise_serializer = ExerciseSerializer(exercise_data)
    return JsonResponse(exercise_serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_word_progress_view(request: Request) -> HttpResponse:
    """Update word study assessment view."""
    serializer = WordAssessmentSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    WordAssessment(request.user, serializer.data).update()
    return HttpResponse(status=HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_word_favorites_view(request: Request) -> HttpResponse:
    """Update word favorites status view."""
    serializer = WordFavoritesSerializer(data=request.data)
    if serializer.is_valid():
        update_word_favorites_status(
            word_id=serializer.data['id'],
            user_id=request.user.pk,
        )
        return HttpResponse(status=HTTP_204_NO_CONTENT)
