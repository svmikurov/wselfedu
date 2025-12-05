"""Contains Lang app models."""

__all__ = [
    'LangExercise',
    'LangMark',
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
from .mark import LangMark
from .params import Params
from .progress import EnglishProgress
from .translation import EnglishTranslation
from .word import EnglishWord, NativeWord

TRANSLATION_MODELS: dict[types.Language, Type[Model]] = {
    'english': EnglishTranslation,
}
PROGRESS_MODELS: dict[types.Language, Type[Model]] = {
    'english': EnglishProgress,
}
