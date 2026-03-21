"""Language discipline schemas."""

__all__ = [
    'WordStudyStoredCase',
    # Presentation
    'LookupCondition',
    'ParametersSchema',
    'SettingsModel',
    'SettingsSchema',
    'RegularConditionRequest',
    'UpdateProgress',
    # Test
    'TestCase',
    'Explanation',
    'TestRequestDTO',
    'TestResponseData',
    'DetailTestRequestDTO',
]

from apps.core.domains.exercise.schema.dto import (
    DetailTestRequestDTO,
    Explanation,
    TestCase,
    TestRequestDTO,
    TestResponseData,
)

from ...core.domains.exercise.schema.parameters import (
    LookupCondition,
    ParametersSchema,
    RegularConditionRequest,
    SettingsModel,
    SettingsSchema,
)
from .progress import UpdateProgress
from .schemas import WordStudyStoredCase
