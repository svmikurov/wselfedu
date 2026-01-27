"""Exercise schemas."""

from pydantic import BaseModel

from .test import OptionId, OptionText


class ExerciseData(BaseModel):
    """Translation test exercise data."""

    question_option: int
    translation_id: int
    question: str
    answer: str
    id_options: list[OptionId]
    text_options: list[OptionText]
