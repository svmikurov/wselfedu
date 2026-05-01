"""Presentation exercise handler response contracts."""

from contracts.enums import ExerciseStatus
from contracts.schemas.base import BaseDTO
from interfaces.schemas.domain.exercise import Option
from interfaces.schemas.response.web.generic import OobResponseDTO

from ._types import AdaptedDomainResultT
from .null import NullContext

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
"""Presentation exercise task response contract.

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
"""Presentation exercise task response contract.
"""

TestExerciseTaskResponse = ExerciseTaskResponse[TestTaskSchema]
"""Test exercise task response contract.
"""
