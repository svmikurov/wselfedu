"""Contains Lang app models."""

__all__ = [
    'LangExercise',
    'LangLabel',
    'NativeWord',
    'EnglishWord',
    'EnglishTranslation',
    'LangCategory',
    'Params',
    'EnglishProgress',
]

from typing import Type

from django.db.models import Model

from apps.lang import types

from .category import LangCategory
from .exercise import LangExercise
from .label import LangLabel
from .params import Params
from .progress import EnglishProgress
from .translation import EnglishTranslation
from .word import EnglishWord, NativeWord

TRANSLATION_MODELS: dict[types.LanguageType, Type[Model]] = {
    'english': EnglishProgress,
}
