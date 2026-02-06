"""Core exercise domain."""

__all__ = [
    # --------------------
    # Enumeration
    # --------------------
    'CaseStatus',
    'DisplayOrder',
    # --------------------
    # Data Transfer Object
    # --------------------
    # General
    'ProgressConfigSchema',
    'UUIDMixin',
    # Presentation
    'PresentationCase',
    'PresentationData',
    'PresentationMeta',
    # Test
    'TestExerciseCase',
    'TestExerciseMeta',
    'TestExerciseData',
    'TestExerciseExplanation',
    # --------------------
    # Exercise
    # --------------------
    # Presentation
    'PresentationDomain',
    # Test
    'RegularTestCreateDomain',
    'DetailTestCreateDomain',
    'TestCheckDomain',
]

from .dto import (
    ProgressConfigSchema,
    UUIDMixin,
)
from .enums import (
    CaseStatus,
    DisplayOrder,
)
from .presentation import (
    PresentationDomain,
)
from .presentation_dto import (
    PresentationCase,
    PresentationData,
    PresentationMeta,
)
from .test import (
    DetailTestCreateDomain,
    RegularTestCreateDomain,
    TestCheckDomain,
)
from .test_dto import (
    TestExerciseCase,
    TestExerciseData,
    TestExerciseExplanation,
    TestExerciseMeta,
)
