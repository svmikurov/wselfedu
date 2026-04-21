"""General WEB exercise request contracts."""

from apps.core.domains.dto import BaseDTO

from .mixins import ExerciseProcessField


class CreateExerciseRequestDTO(
    ExerciseProcessField,
    BaseDTO,
):
    """Create exercise request DTO.

    Parameter
    ---------
    action : `ExerciseProcessEnum`
        Process exercise action.

    """
