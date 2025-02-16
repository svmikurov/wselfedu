"""User REST views."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from users.models.points import get_points_balance
from users.serializers.points import PointsSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def render_user_data(request: Request) -> Response:
    """Render the user data view."""
    user = request.user
    data = {
        'points': get_points_balance(user.pk),
    }
    serializer = PointsSerializer(data)
    return Response(serializer.data, status=HTTP_200_OK)
