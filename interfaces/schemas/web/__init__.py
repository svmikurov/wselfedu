"""Web schemas."""

__all__ = (
    # Response's components
    'PresentationTaskSchema',
    'TestTaskSchema',
    # Response's compositions
    'PresentationTaskResponse',
    'TestExerciseTaskResponse',
)


from .task import (
    PresentationTaskResponse,
    PresentationTaskSchema,
    TestExerciseTaskResponse,
    TestTaskSchema,
)
