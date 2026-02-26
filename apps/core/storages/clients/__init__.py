"""Contains storage clients."""

__all__ = [
    # ABC
    'CacheABC',
    # Implementation
    'DjangoCache',
]

from .django_cache import DjangoCache
from .iabc import CacheABC
