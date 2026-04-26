"""Presentation exercise handler response contracts."""

from interfaces.enums.exercise import ExerciseStatus
from interfaces.schemas.base import NullDTO
from interfaces.schemas.domain.exercise.task import PresentationTask
from interfaces.schemas.response.generic import OobResponseDTO

PresentationTaskResponse = OobResponseDTO[
    ExerciseStatus,
    PresentationTask,
    NullDTO,
]
"""Presentation exercise task response contract.

Parameter
---------
domain_status : `ExerciseStatusEnum`
    Domain result status.
context : `AdaptedDomainResultT`
    Response context with adapted domain result data.
extra_context : `NulDTO`
    Extra context for response.
oob_html : `str`
    Out Of Band html.

"""
