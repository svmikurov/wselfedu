"""Language discipline schemas."""

from pydantic import BaseModel

from . import types


class ProgressConfigSchema(BaseModel):
    """Iem study progress config schema."""

    increment: int
    decrement: int


class WordStudyStoredCase(BaseModel):
    """Word study schema for store.

    Scheme of temporary storage of the word study
    exercise being performed.
    """

    translation_id: int
    language: types.Language
