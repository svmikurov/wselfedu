"""Exercise task's WEB response interfaces."""

from typing import TypeVar

from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.domain.exercise.fields import (
    DefineField,
    MeanField,
    Option,
    ProgressValueField,
    QuestionTextField,
)
from ports.interfaces.schemas.response.web.generic import HtmlResponseDTO
from ports.interfaces.schemas.response.web.null import NullContext

__all__ = (
    # Response's components
    'PresentationTaskContext',
    'TestTaskContext',
    # Response's compositions
    'PresentationTaskResponse',
    'TestExerciseTaskResponse',
)

AdaptedDomainResultT = TypeVar('AdaptedDomainResultT')


# =================================================
# Response's components
# =================================================


class PresentationTaskContext(
    DefineField,
    MeanField,
    ProgressValueField,
):
    """Presentation task web schema.

    Parameter
    ---------
    define : `str`
    mean : `str`
    progress_value: `int`
    """


class TestTaskContext(
    QuestionTextField,
):
    """Presentation task web schema.

    Parameter
    ---------
    question_text : `str
        Question text.
    options : `list[Option]`
        Task options (value, text).
    """

    options: list[Option]


# =================================================
# Response's generics
# =================================================


ExerciseTaskResponse = HtmlResponseDTO[
    ExerciseStatus,
    AdaptedDomainResultT,
    NullContext,
]
"""Presentation exercise task response interfaces.

Parameters
----------
domain_status : `ExerciseStatusEnum`
    Domain result status.
context : `AdaptedDomainResultT`
    Response context with adapted domain result data.
extra_context : `NullContext`
    Extra context for response.
html : `str`
    Html.

"""


# =================================================
# Response's compositions
# =================================================


PresentationTaskResponse = ExerciseTaskResponse[PresentationTaskContext]
"""Presentation exercise task response interface.
"""

TestExerciseTaskResponse = ExerciseTaskResponse[TestTaskContext]
"""Test exercise task response interface.
"""
