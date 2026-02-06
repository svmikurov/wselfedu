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

from .presentation import (
    LookupCondition,
    ParametersSchema,
    RegularConditionRequest,
    SettingsModel,
    SettingsSchema,
)
from .progress import UpdateProgress
from .schemas import WordStudyStoredCase
from .test import (
    DetailTestRequestDTO,
    Explanation,
    TestCase,
    TestRequestDTO,
    TestResponseData,
)
