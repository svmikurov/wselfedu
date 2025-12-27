"""Custom API renderers."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Final

from django.http import HttpResponse
from rest_framework import renderers, status

if TYPE_CHECKING:
    from .types import (
        AcceptedMediaType,
        JsonEncodedResponse,
        JsonResponseWrap,
        OriginalResponseData,
        RendererContext,
    )


# Template for successful responses
SUCCESS_WRAP_TEMPLATE: Final[JsonResponseWrap] = {
    'status': 'success',
    'message': 'Success',
    'code': None,
    'data': None,
}

# Template for error responses
ERROR_WRAP_TEMPLATE: Final[JsonResponseWrap] = {
    'status': 'error',
    'message': 'Error',
    'code': None,
    'data': None,
    'errors': None,
}


class WrappedJSONRenderer(renderers.JSONRenderer):
    """JSON renderer to wrap API responses in a standardized format.

    For 204 No Content responses, an empty byte string is returned.
    """

    def render(
        self,
        data: OriginalResponseData,
        accepted_media_type: AcceptedMediaType = None,
        renderer_context: RendererContext = None,
    ) -> JsonEncodedResponse:
        """Render the wrapped JSON response."""
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)  # type: ignore[no-any-return]

        response = renderer_context.get('response')

        if not isinstance(response, HttpResponse):
            return super().render(data, accepted_media_type, renderer_context)  # type: ignore[no-any-return]

        match status_code := response.status_code:
            case status.HTTP_204_NO_CONTENT:
                return b''

            case status_code if status_code < HTTPStatus.BAD_REQUEST:
                wrapped_data = self._wrap_success(data=data)

            case _:
                wrapped_data = self._wrap_error(data=data)

        return super().render(  # type: ignore[no-any-return]
            wrapped_data, accepted_media_type, renderer_context
        )

    def _wrap_success(self, data: OriginalResponseData) -> JsonResponseWrap:
        payload: JsonResponseWrap = SUCCESS_WRAP_TEMPLATE.copy()

        match data:
            case {'detail': detail}:
                payload['message'] = detail
                if hasattr(detail, 'code'):
                    payload['code'] = detail.code

            case _:
                payload['data'] = data

        return payload

    def _wrap_error(self, data: OriginalResponseData) -> JsonResponseWrap:
        payload: JsonResponseWrap = ERROR_WRAP_TEMPLATE.copy()

        match data:
            case {'detail': detail}:
                payload['message'] = detail
                if hasattr(detail, 'code'):
                    payload['code'] = detail.code

            case {'errors': _} | {'non_field_errors': _}:
                payload['message'] = 'Validation error'
                payload['errors'] = data

            case _:
                payload['message'] = 'Unexpected server error'

        return payload
