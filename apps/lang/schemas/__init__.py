"""Language discipline schemas."""

__all__ = [
    'WordStudyStoredCase',
    'ProgressConfigSchema',
    # Presentation
    'ParametersModel',
    'ParametersSchema',
    'SettingsModel',
    'SettingsSchema',
    'PresentationRequest',
    'UpdateProgress',
    # Test
    'Case',
    'CaseStatus',
    'Explanation',
    'TestRequestDTO',
    'TestResponseData',
    'DetailTestRequestDTO',
]

from .presentation import (
    ParametersModel,
    ParametersSchema,
    PresentationRequest,
    SettingsModel,
    SettingsSchema,
)
from .progress import UpdateProgress
from .schemas import ProgressConfigSchema, WordStudyStoredCase
from .test import (
    Case,
    CaseStatus,
    DetailTestRequestDTO,
    Explanation,
    TestRequestDTO,
    TestResponseData,
)
