"""Custom API renderers."""

from http import HTTPStatus
from typing import Any, Mapping

from django.http import HttpResponse
from rest_framework import renderers, status


class WrappedJSONRenderer(renderers.JSONRenderer):
    """Wrapped JSON response renderer."""

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

        if status_code == status.HTTP_204_NO_CONTENT:
            return b''

        status_text = (
            'success' if status_code < HTTPStatus.BAD_REQUEST else 'error'
        )
        message = renderer_context.get('message')

        if status_text == 'success':
            wrapped_data = self._wrap_success(
                data=data,
                status_code=status_code,
                message=message,
            )
        else:
            wrapped_data = self._wrap_error(
                data=data,
                status_code=status_code,
                message=message,
            )

        return super().render(
            wrapped_data, accepted_media_type, renderer_context
        )

    def _wrap_success(
        self,
        data: object,
        status_code: int,
        message: str | None = None,
    ) -> dict[str, Any]:
        default_message: str = 'Success'

        return {
            'status': 'success',
            'code': status_code,
            'message': message or default_message,
            'data': data,
        }

    def _wrap_error(
        self,
        data: object,
        status_code: int,
        message: str | None = None,
    ) -> dict[str, Any]:
        default_message: str = 'Error'

        if isinstance(data, dict):
            if 'detail' in data:
                default_message = message or data['detail']
            elif any(key in data for key in ['errors', 'non_field_errors']):
                default_message = message or 'Validation error'

        return {
            'status': 'error',
            'code': status_code,
            'message': message or default_message,
            'data': None,
            'errors': data,
        }
