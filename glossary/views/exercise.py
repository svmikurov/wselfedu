"""Glossary exercise view."""

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
    ACTION,
    CATEGORIES,
    DEFAULT_LOOKUP_CONDITIONS,
    EDGE_PERIOD_ALIASES,
    EDGE_PERIOD_ITEMS,
    ERROR,
    EXERCISE_CHOICES,
    GET,
    ID,
    LOOKUP_CONDITIONS,
    MSG_NO_TASK,
    NO_SELECTION,
    POST,
    PROGRES_STEPS,
    PROGRESS,
    PROGRESS_ALIASES,
    PROGRESS_MAX,
    PROGRESS_MIN,
    USER_ID,
)
from glossary.exercise.question import (
    GlossaryExerciseGUI,
)
from glossary.models import (
    Glossary,
    GlossaryCategory,
    GlossaryParams,
)
from glossary.serializers import (
    GlossaryCategorySerializer,
    GlossaryParamsSerializer,
)


@api_view([POST])
@permission_classes((permissions.AllowAny,))
def glossary_exercise(request: Request) -> JsonResponse | HttpResponse:
    """Render the Glossary exercise."""
    serializer = GlossaryParamsSerializer(data=request.data)

    if serializer.is_valid():
        lookup_conditions = serializer.data
        lookup_conditions[USER_ID] = request.user.id
        try:
            exercise = GlossaryExerciseGUI(lookup_conditions).task_data
        except IndexError:
            error = {ERROR: MSG_NO_TASK}
            return JsonResponse(error, status=HTTP_400_BAD_REQUEST)

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
            user_params = GlossaryParams.objects.get(user=user)
        except GlossaryParams.DoesNotExist:
            lookup_conditions = DEFAULT_LOOKUP_CONDITIONS
        else:
            lookup_conditions = GlossaryParamsSerializer(user_params).data

        try:
            queryset = GlossaryCategory.objects.filter(user=user)
        except GlossaryCategory.DoesNotExist:
            queryset = GlossaryCategory.objects.none()
        categories = GlossaryCategorySerializer(queryset, many=True).data
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
        serializer = GlossaryParamsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            if not serializer.is_created:
                return Response(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view([POST])
@permission_classes((permissions.AllowAny,))
def update_term_study_progress(request: HttpRequest) -> HttpResponse:
    """Update term study progres."""
    user = request.user
    payload = JSONParser().parse(request)
    term_pk = payload.get(ID)

    try:
        term = Glossary.objects.get(pk=term_pk)
    except Glossary.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        # Only owner have access to his term.
        if user != term.user:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    action = payload.get(ACTION)
    progress_delta = PROGRES_STEPS.get(action)
    updated_progress = term.progress + progress_delta

    if PROGRESS_MIN <= updated_progress <= PROGRESS_MAX:
        term.progress = updated_progress
        term.save(update_fields=[PROGRESS])

    return HttpResponse(status=status.HTTP_200_OK)
