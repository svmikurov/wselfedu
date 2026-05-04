"""Web schemas."""

__all__ = (
    # Response's components
    'PresentationTaskContext',
    'TestTaskContext',
    # Response's compositions
    'PresentationTaskResponse',
    'TestExerciseTaskResponse',
)


from .task import (
    PresentationTaskContext,
    PresentationTaskResponse,
    TestExerciseTaskResponse,
    TestTaskContext,
)
