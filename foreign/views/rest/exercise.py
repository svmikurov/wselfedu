"""Translate foreign word exercise DRF views."""

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK

from config.constants import (
    CATEGORIES,
    DEFAULT_LOOKUP_CONDITIONS,
    EDGE_PERIOD_ALIASES,
    EDGE_PERIOD_ITEMS,
    EXERCISE_CHOICES,
    GET,
    LOOKUP_CONDITIONS,
    POST,
    PROGRESS,
    PROGRESS_ALIASES,
)
from foreign.models import TranslateParams, WordCategory
from foreign.serializers import (
    TranslateParamsSerializer,
    WordCategorySerializer,
)


@api_view([GET, POST])
@permission_classes((permissions.IsAuthenticated,))
def exercise_parameters(request: Request) -> JsonResponse:
    """Render the Translate word exercise params the DRF view.

    GET method
    ----------
    View renders a response with ``exercise_params``.

    Fields:
    - :term:`lookup_conditions`
    - :term:`exercise_choices`
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

        exercise_params = {
            LOOKUP_CONDITIONS: lookup_conditions,
            EXERCISE_CHOICES: {
                EDGE_PERIOD_ITEMS: EDGE_PERIOD_ALIASES,
                CATEGORIES: categories,
                PROGRESS: PROGRESS_ALIASES,
            },
        }

        return JsonResponse(exercise_params, status=HTTP_200_OK)


# def translate_exercise(request: Request) -> JsonResponse:
#     """Render the Translate foreign word exercise the DRF view."""
#     serializer = TranslateParamsSerializer(data=request.data)
