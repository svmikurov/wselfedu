"""Request's data validator's interface."""

__all__ = (
    'CreateTaskSchema',
    'CheckTestAnswerSchema',
    'ProgressUpdateSchema',
)

from .task import (
    CheckTestAnswerSchema,
    CreateTaskSchema,
    ProgressUpdateSchema,
)
