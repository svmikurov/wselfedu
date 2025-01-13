"""Term exercise view."""

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from config.constants import (
    MSG_NO_TASK,
    PROGRES_STEPS,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from foreign.serializers import ExerciseSerializer
from glossary.exercise.question import (
    GlossaryExerciseGUI,
)
from glossary.models import (
    GlossaryParams,
    Term,
)
from glossary.serializers import (
    GlossaryExerciseParamSerializer,
    TermParamsSerializer,
)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def glossary_exercise_view(request: Request) -> JsonResponse | HttpResponse:
    """Render the Term exercise."""
    # Get exercise parameters.
    params_serializer = GlossaryExerciseParamSerializer(data=request.data)
    params_serializer.is_valid()
    # Create exercise task.
    lookup_conditions = params_serializer.data
    lookup_conditions['user_id'] = request.user.pk
    try:
        exercise_data = GlossaryExerciseGUI(lookup_conditions).exercise_data
    except IndexError:
        data = {'details': MSG_NO_TASK}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    else:
        exercise_serializer = ExerciseSerializer(exercise_data)
        return Response(data=exercise_serializer.data)


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

    elif request.method == 'PUT':
        serializer = TermParamsSerializer(
            data=request.data, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(user=user)

            if serializer.is_created:
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(status=HTTP_204_NO_CONTENT)

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
