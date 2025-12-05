"""Custom exception handler."""

from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.core.exceptions import info


def custom_exception_handler(
    exc: Exception,
    context: dict[str, object],
) -> Response | None:
    """Handle exceptions."""
    if response := exception_handler(exc, context):
        return response

    match exc:
        case info.NoTranslationsAvailableException:
            return Response()
        case _:
            return None
