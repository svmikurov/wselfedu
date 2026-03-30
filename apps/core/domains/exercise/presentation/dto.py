"""Core presentation DTOs."""

from apps.core.domains.dto import (
    BaseDTO,
)

from .. import dto


class PresentationCase(
    dto.ExerciseStatusSchema,
    dto.QuestionTextField,
    dto.AnswerTextField,
    dto.ProgressValueField,
    BaseDTO,
):
    """Presentation exercise case.

    Parameter
    ---------
    status : `ExerciseStatusEnum`
        Current exercise performing status.
    question_text : `str`
        Exercise question text.
    answer_text : `str`
        Exercise answer text.
    progress_value: `int`
        Current item study progress value.

    """


class PresentationMeta(
    dto.ResourceIdentifierField,
    BaseDTO,
):
    """Presentation exercise meta.

    Parameter
    ---------
    pk : `int`
        Stored presentation exercise database identifier.

    """
