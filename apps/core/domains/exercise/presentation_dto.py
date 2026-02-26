"""Core presentation DTOs."""

from pydantic import Field

from ..base_dto import BaseDTO, ProtectDefaultStatusMixin
from . import ExerciseStatusEnum, UuidDTO

# -----------------------------------
# Presentation exercise domain result
# ------------------=----------------


class PresentationCase(ProtectDefaultStatusMixin, BaseDTO):
    """Presentation exercise case."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE,
        description='Exercise status',
    )

    question_text: str = Field(
        description='Display question text',
    )
    answer_text: str = Field(
        description='Display answer text',
    )

    progress: int = Field(
        description='Item study progress',
    )


class PresentationMeta(BaseDTO):
    """Presentation exercise meta."""

    pk: int = Field(description='Database presentation item ID')


class PresentationData(UuidDTO, PresentationCase):
    """Presentation case for rendering to the user."""
