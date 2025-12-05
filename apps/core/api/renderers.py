"""Custom API renderers."""

from http import HTTPStatus
from typing import Any, Mapping

from django.http import HttpResponse
from rest_framework import renderers, status


class WrappedJSONRenderer(renderers.JSONRenderer):
    """Wrapped JSON response renderer."""

    def render(
        self,
        data: dict[str, Any],
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, Any] | None = None,
    ) -> Any:  # noqa: ANN401
        """Render the wrapped JSON response."""
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get('response')

        if not isinstance(response, HttpResponse):
            return super().render(data, accepted_media_type, renderer_context)

        match status_code := response.status_code:
            case status.HTTP_204_NO_CONTENT:
                return b''

            case status_code if status_code < HTTPStatus.BAD_REQUEST:
                wrapped_data = self._wrap_success(data=data)

            case _:
                wrapped_data = self._wrap_error(data=data)

        return super().render(
            wrapped_data, accepted_media_type, renderer_context
        )

    def _wrap_success(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            'status': 'success',
            'message': 'Success',
            'data': None,
        }

        match data:
            case {'detail': detail}:
                payload['message'] = detail
                payload['code'] = detail.code

            case _:
                payload['data'] = data

        return payload

    def _wrap_error(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            'status': 'error',
            'data': None,
        }

        match data:
            case {'detail': detail}:
                payload['message'] = detail
                payload['code'] = detail.code

            case {'errors': _} | {'non_field_errors': _}:
                payload['message'] = 'Validation error'
                payload['errors'] = data

            case _:
                payload['message'] = 'Unexpected server error'

        return payload
