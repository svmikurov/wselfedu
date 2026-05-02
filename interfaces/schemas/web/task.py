"""Presentation exercise handler response interfaces."""

from contracts.enums import ExerciseStatus
from contracts.schemas.base import BaseDTO
from contracts.schemas.response.generic import OobResponseDTO
from contracts.schemas.response.null import NullContext
from contracts.schemas.response.types import AdaptedDomainResultT
from interfaces.schemas.domain.exercise import Option

# =================================================
# Components
# =================================================


class PresentationTaskSchema(BaseDTO):
    """Presentation task web schema."""

    define: str
    mean: str
    progress: int


class TestTaskSchema(BaseDTO):
    """Presentation task web schema."""

    question: str
    options: list[Option]


# =================================================
# Compositions
# =================================================

ExerciseTaskResponse = OobResponseDTO[
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
oob_html : `str`
    Out Of Band html.

"""


PresentationTaskResponse = ExerciseTaskResponse[PresentationTaskSchema]
"""Presentation exercise task response interface.
"""

TestExerciseTaskResponse = ExerciseTaskResponse[TestTaskSchema]
"""Test exercise task response interface.
"""
