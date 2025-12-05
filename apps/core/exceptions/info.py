"""Info exceptions."""

from rest_framework import status
from rest_framework.exceptions import APIException

from .codes import Code


class NoTranslationsAvailableException(APIException):
    """No available translations for requested lookup conditions."""

    status_code = status.HTTP_200_OK
    default_detail = (
        'There are no translations available '
        'for the requested lookup conditions.'
    )
    default_code = Code.NO_CASES
