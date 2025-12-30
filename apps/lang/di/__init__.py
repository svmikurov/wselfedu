"""Language app DI container."""

__all__ = [
    # Language app main DI container
    'LanguageContainer',
    # Language app DI containers
    'PresentationContainer',
    'TranslationTestContainer',
]

from .container import LanguageContainer
from .translation_presentation import PresentationContainer
from .translation_test import TranslationTestContainer
