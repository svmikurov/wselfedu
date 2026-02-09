"""Request handlers."""

__all__ = [
    'SimpleRequestHandler',
    'DetailRequestHandler',
    'RegularRequestHandler',
]
from .generic import (
    DetailRequestHandler,
    RegularRequestHandler,
    SimpleRequestHandler,
)
