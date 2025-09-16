"""Custom API renderers."""

from http import HTTPStatus
from typing import Any, Mapping

from django.http import HttpResponse
from rest_framework import renderers


class WrappedJSONRenderer(renderers.JSONRenderer):
    """Wrapped JSON response renderer.

    This renderer wraps API responses in a format:
    {
        "status": "success" | "error",
        "message": string,
        "data": ...
    }

    For example:

        class SomeView(ModelViewSet):
            ...
            renderer_classes = [WrappedJSONRenderer]
    """

    def render(
        self,
        data: object,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, Any] | None = None,
    ) -> Any:  # noqa: ANN401
        """Render the wrapped JSON response."""
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get('response')
        if not isinstance(response, HttpResponse):
            return super().render(data, accepted_media_type, renderer_context)

        status_code = response.status_code
        status = 'success' if status_code < HTTPStatus.BAD_REQUEST else 'error'
        message = renderer_context.get('message')

        wrapped_data: dict[str, Any] = {
            'status': status,
            'message': message,
            'data': data,
        }

        return super().render(
            wrapped_data,
            accepted_media_type,
            renderer_context,
        )
