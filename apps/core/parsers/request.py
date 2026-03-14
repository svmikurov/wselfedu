"""Request parameters parser."""

from typing import TypedDict, TypeVar

from apps.core.handlers.dto import RequestParams

from .abstract import AbstractRequestParser

Parsed = TypeVar('Parsed')


class DetailRequestParamsType(TypedDict):
    """Detail request parameters typed dict."""

    pk: str


class NullParser(
    AbstractRequestParser[RequestParams, RequestParams],
):
    """Detail request parameters parser."""

    def parse(self, params: RequestParams) -> RequestParams:
        """Parse detail request parameters."""
        return params
