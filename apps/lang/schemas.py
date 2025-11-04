"""Language discipline schemas."""

from pydantic import BaseModel

from . import types


class ProgressConfigSchema(BaseModel):
    """Iem study progress config schema."""

    increment: int
    decrement: int


class WordStudyCaseSchema(BaseModel):
    """Word study schema."""

    translation_id: int
    language: types.LanguageType


class UpdateWordProgressSchema(BaseModel):
    """Update word study progress schema."""

    translation_id: int
    language: types.LanguageType
    progress_case: types.ProgressType
    progress_value: int
