"""Language discipline adapters."""

__all__ = [
    # ABC
    'BaseTranslationAdapterWEB',
    # Implementation
    'TranslationAdapterWEB',
]

from .web.base import BaseTranslationAdapterWEB
from .web.presentation import TranslationAdapterWEB
