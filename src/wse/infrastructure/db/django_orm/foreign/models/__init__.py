"""Foreign application models."""

__all__ = (
    'NativeWord',
    'EnglishWord',
    'EnglishTranslation',
)

from .translation import EnglishTranslation
from .word import EnglishWord, NativeWord
