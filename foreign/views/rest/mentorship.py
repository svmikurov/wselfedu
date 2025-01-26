"""Foreign words mentorship views."""

import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK

from contrib.views.views_rest import IsOwner
from foreign.exercise.testing import ItemTesting


def foreign_assignation_main_view(request: HttpRequest) -> HttpResponse:
    """Return assignations foreign mentorship."""
    pass


@api_view(['GET'])
@permission_classes((IsOwner,))
def foreign_assigned_test_view(request: HttpRequest) -> JsonResponse:
    """Return assigned foreign word test."""
    data = ItemTesting(request.user).task_data
    json_data = json.dumps(data)
    return JsonResponse(data=json_data, status=HTTP_200_OK, safe=False)
