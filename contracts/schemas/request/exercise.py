"""General WEB exercise request contracts."""

from contracts.schemas.domain.exercise.fields import (
    ExerciseActionField,
)


class ExerciseRequestDTO(
    ExerciseActionField,
):
    """Create exercise request DTO.

    Parameter
    ---------
    action : `ExerciseProcessEnum`
        Process exercise action.

    """
