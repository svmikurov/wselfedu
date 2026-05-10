"""Exercise task's WEB response interfaces."""

from contracts.schemas.domain.exercise.fields import (
    DefineField,
    MeanField,
    ProgressValueField,
    QuestionTextField,
)
from contracts.schemas.fields import TextField, ValueField
from contracts.schemas.response.generic import HtmlResponseDTO
from contracts.schemas.response.null import NullContext
from contracts.schemas.response.types import AdaptedDomainResultT
from ports.contract.enums import ExerciseStatus

__all__ = (
    # Response's components
    'PresentationTaskContext',
    'TestTaskContext',
    # Response's compositions
    'PresentationTaskResponse',
    'TestExerciseTaskResponse',
)

# =================================================
# Response's components
# =================================================


class Option(ValueField, TextField):
    """Test exercise option schema.

    Parameter
    ---------
    value : `int`
        Option value.
    text : `str`
        Option text.
    """


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
    Options : `list[Option]`
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
