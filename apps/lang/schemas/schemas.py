"""Language discipline schemas."""

from pydantic import BaseModel

from ports.refactor.lang import types


class WordStudyStoredCase(BaseModel):
    """Word study schema for store.

    Scheme of temporary storage of the word study
    exercise being performed.
    """

    translation_id: int
    language: types.Language
