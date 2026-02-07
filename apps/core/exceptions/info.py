"""Info exceptions."""

from rest_framework import status
from rest_framework.exceptions import APIException

from .codes import Code


class NoExerciseItemsException(APIException):
    """No available items for exercise requested lookup conditions."""

    status_code = status.HTTP_200_OK
    default_detail = (
        'There are no items available for exercise '
        'with requested lookup conditions.'
    )
    default_code = Code.NO_CASES
