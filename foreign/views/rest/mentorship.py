"""Foreign words mentorship views."""

import json

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request

from contrib.views.views_rest import IsOwner
from foreign.exercise.testing import ItemTesting
from foreign.serializers.mentorship import ItemTestingAnswerSerializer

CACHE_KEY = 'word_test_%s'
CACHE_TIMEOUT = 600


def foreign_assignation_main_view(request: Request) -> HttpResponse:
    """Return assignations foreign mentorship."""
    pass


@api_view(['GET', 'POST'])
@permission_classes((IsOwner,))
def foreign_assigned_test_view(
    request: Request,
) -> JsonResponse | HttpResponse:
    """Return assigned foreign word test."""
    user = request.user
    cache_key = CACHE_KEY % user.username

    if request.method == 'GET':
        data = ItemTesting(user).task_data
        cache.set(cache_key, data.get('answer'), CACHE_TIMEOUT)
        json_data = json.dumps(data)
        return JsonResponse(
            data=json_data,
            status=status.HTTP_200_OK,
            safe=False,
        )

    elif request.method == 'POST':
        serializer = ItemTestingAnswerSerializer(data=request.data)

        if serializer.is_valid():
            correct_answer = cache.get(cache_key)
            user_answer = request.data['answer']

            if correct_answer == user_answer:
                return HttpResponse(
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return HttpResponse(
                    status=status.HTTP_205_RESET_CONTENT,
                )

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
