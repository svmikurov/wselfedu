"""Core exercise domain."""

__all__ = [
    # --------------------
    # Enumeration
    # --------------------
    'ExerciseStatusEnum',
    'DisplayOrder',
    # --------------------
    # Data Transfer Object
    # --------------------
    # General
    'ProgressConfigSchema',
    'UuidDTO',
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
    UuidDTO,
)
from .enums import (
    DisplayOrder,
    ExerciseStatusEnum,
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
