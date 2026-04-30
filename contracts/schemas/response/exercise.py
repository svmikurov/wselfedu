"""Presentation exercise handler response contracts."""

from contracts.enums import ExerciseStatus
from contracts.schemas.domain.exercise import dtos
from contracts.schemas.response.generic import OobResponseDTO

from ._types import AdaptedDomainResultT, CandidatesT
from .general import NullContext

ExerciseTaskResponse = OobResponseDTO[
    ExerciseStatus,
    AdaptedDomainResultT,
    NullContext,
]
"""Presentation exercise task response contract.

Parameter
---------
domain_status : `ExerciseStatusEnum`
    Domain result status.
context : `AdaptedDomainResultT`
    Response context with adapted domain result data.
extra_context : `NullContext`
    Extra context for response.
oob_html : `str`
    Out Of Band html.

"""


PresentationTaskResponse = ExerciseTaskResponse[dtos.PresentationTask]
"""Presentation exercise task response contract.
"""

TestExerciseTaskResponse = ExerciseTaskResponse[
    dtos.TestExerciseTask[CandidatesT],
]
"""Test exercise task response contract.
"""
