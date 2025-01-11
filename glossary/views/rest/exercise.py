"""Term exercise view."""

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from config.constants import (
    MSG_NO_TASK,
    PROGRES_STEPS,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from glossary.exercise.question import (
    GlossaryExerciseGUI,
)
from glossary.models import (
    GlossaryParams,
    Term,
)
from glossary.serializers import (
    TermParamsSerializer,
)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def glossary_exercise(request: Request) -> JsonResponse | HttpResponse:
    """Render the Term exercise."""
    serializer = TermParamsSerializer(data=request.data)

    if serializer.is_valid():
        lookup_conditions = serializer.data
        lookup_conditions['user_id'] = request.user.id
        try:
            exercise = GlossaryExerciseGUI(lookup_conditions).task_data
        except IndexError:
            error = {'error': MSG_NO_TASK}
            return JsonResponse(error, status=HTTP_400_BAD_REQUEST)

        return JsonResponse(exercise, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes((permissions.AllowAny,))
def glossary_params_view(
    request: Request,
) -> JsonResponse | HttpResponse:
    """Term exercise parameters view."""
    user = request.user

    if request.method == 'GET':
        params, _ = GlossaryParams.objects.get_or_create(user=user)
        serializer = TermParamsSerializer(params, context={'request': request})
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        serializer = TermParamsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if not serializer.is_created:
                return Response(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def update_term_study_progress(request: HttpRequest) -> HttpResponse:
    """Update term study progres."""
    user = request.user
    payload = JSONParser().parse(request)
    term_pk = payload.get('id')

    try:
        term = Term.objects.get(pk=term_pk)
    except Term.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        # Only owner have access to his term.
        if user != term.user:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    action = payload.get('action')
    progress_delta = PROGRES_STEPS.get(action)
    updated_progress = term.progress + progress_delta

    if PROGRESS_MIN <= updated_progress <= PROGRESS_MAX:
        term.progress = updated_progress
        term.save(update_fields=['progress'])

    return HttpResponse(status=status.HTTP_200_OK)
