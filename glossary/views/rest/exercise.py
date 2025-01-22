"""Term exercise view."""

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from config.constants import (
    MSG_NO_TASK,
    PROGRES_STEPS,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from contrib.views.views_rest import IsOwner
from glossary.exercise.question import (
    GlossaryExerciseGUI,
)
from glossary.models import (
    GlossaryParams,
    Term,
)
from glossary.queries.lookup_params import TermLookupParams
from glossary.serializers import (
    ExerciseSerializer,
    GlossaryExerciseParamsSerializer,
    TermFavoritesSerializer,
    TermParamsSerializer,
    TermSerializer,
)


@api_view(['GET', 'PUT'])
@permission_classes((IsOwner,))
def glossary_params_view(request: Request) -> JsonResponse | HttpResponse:
    """Glossary exercise parameters view."""
    context = {'request': request}

    if request.method == 'GET':
        params, _ = GlossaryParams.objects.get_or_create(user=request.user)
        serializer = TermParamsSerializer(params, context=context)
        return JsonResponse(serializer.data, status=HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data
        serializer = TermParamsSerializer(data=data, context=context)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if serializer.is_created:
                return JsonResponse(serializer.data, status=HTTP_201_CREATED)
            return HttpResponse(status=HTTP_204_NO_CONTENT)

        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsOwner,))
def glossary_selected_view(request: Request) -> JsonResponse:
    """Render the selected terms for exercise."""
    request_serializer = GlossaryExerciseParamsSerializer(data=request.data)
    request_serializer.is_valid()
    lookup_conditions = request_serializer.data
    lookup_conditions['user_id'] = request.user.pk

    is_first = lookup_conditions.pop('is_first')
    is_last = lookup_conditions.pop('is_last')
    count_first = lookup_conditions.pop('count_first')
    count_last = lookup_conditions.pop('count_last')

    lookup_params = TermLookupParams(lookup_conditions).params
    queryset = Term.objects.filter(*lookup_params, user=request.user)

    if is_first and is_last:
        queryset_first = queryset[:count_first]
        queryset_last = queryset.order_by('-pk')[:count_last]
        queryset = queryset_last.union(queryset_first).order_by('pk')
    elif is_first:
        queryset = queryset[:count_first]
    elif is_last:
        queryset = queryset.order_by('-pk')[:count_last]

    queryset = queryset.order_by('-pk')
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result = paginator.paginate_queryset(queryset, request)
    serializer = TermSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes((IsOwner,))
def glossary_exercise_view(request: Request) -> JsonResponse | HttpResponse:
    """Glossary exercise view."""
    params_serializer = GlossaryExerciseParamsSerializer(data=request.data)
    params_serializer.is_valid()
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk

    try:
        exercise_data = GlossaryExerciseGUI(lookup_conditions).task_data
    except IndexError:
        data = {'details': MSG_NO_TASK}
        return HttpResponse(data, status=HTTP_204_NO_CONTENT)

    favorites = Term.objects.get(pk=exercise_data['id']).favorites
    exercise_data['favorites'] = favorites
    exercise_serializer = ExerciseSerializer(exercise_data)
    return JsonResponse(exercise_serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_term_progress_view(request: Request) -> HttpResponse:
    """Update term study progres."""
    payload = JSONParser().parse(request)
    term_pk = payload.get('id')

    try:
        term = Term.objects.get(pk=term_pk)
    except Term.DoesNotExist:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)

    # Check permissions on object
    if term.user != request.user:
        return HttpResponse(status=HTTP_403_FORBIDDEN)

    action = payload.get('action')
    progress_delta = PROGRES_STEPS.get(action)
    updated_progress = term.progress + progress_delta

    if PROGRESS_MIN <= updated_progress <= PROGRESS_MAX:
        term.progress = updated_progress
        term.save(update_fields=['progress'])

    return HttpResponse(status=HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsOwner,))
def update_term_favorites_view(request: Request) -> HttpResponse:
    """Update term favorites status view."""
    serializer = TermFavoritesSerializer(data=request.data)
    serializer.is_valid()

    term_id = serializer.data['id']
    term = Term.objects.get(pk=term_id, user=request.user)
    term.favorites = not term.favorites
    term.save()

    return HttpResponse(status=HTTP_204_NO_CONTENT)
