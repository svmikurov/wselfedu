"""Base exercise views."""

__all__ = (
    # TypeAlias
    'DetailHandler',
    'QueryHandler',
    # Views
    'BaseQueryPerformView',
    'BaseDetailPerformView',
)

from .base import (
    BaseDetailPerformView,
    BaseQueryPerformView,
    DetailHandler,
    QueryHandler,
)
