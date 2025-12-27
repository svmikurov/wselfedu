"""Core api types."""

from typing import Any, Literal, Mapping, NotRequired, TypedDict

# ---------------------------
# Wrapped JSON renderer types
# ---------------------------

type OriginalResponseData = Mapping[str, Any] | list[Any] | None
type AcceptedMediaType = str | None
type RendererContext = Mapping[str, Any] | None
type JsonEncodedResponse = bytes


class JsonResponseWrap(TypedDict):
    """JSON response wrap type."""

    status: Literal['success', 'error']
    message: str
    code: str | None
    data: OriginalResponseData
    errors: NotRequired[OriginalResponseData]
