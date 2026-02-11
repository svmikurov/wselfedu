"""Mathematical discipline domain DTOs."""

from pydantic import BaseModel


class TextCase(BaseModel):
    """Exercise case with text question representation."""

    question_text: str
    answer: int
