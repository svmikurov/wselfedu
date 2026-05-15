"""Test types."""

from typing import Any

from kernel.handler.generic import RequestHandler

PresentationHandlerT = RequestHandler[Any, Any, Any, Any, Any, Any, Any]
