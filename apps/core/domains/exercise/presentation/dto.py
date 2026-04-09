"""Core presentation DTOs."""

from typing import TypeVar

from apps.core.domains.dto import BaseDTO

from .. import dto

OptionT = TypeVar('OptionT')


class PresentationDomainResult(
    dto.OptionField[OptionT],
):
    """Presentation exercise create domain result.

    Parameter
    ---------
    option : ...
        Exercise option field.

    """


class PresentationTask(
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


# DEPRECATED:
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
