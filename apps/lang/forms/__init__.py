"""Language discipline forms."""

__all__ = [
    # Case
    'CaseRequestForm',
    # Parameters
    'ParametersForm',
    'PresentationSettingsForm',
    'PresentationSettingsFormSet',
    'TranslationSettingsForm',
    'TranslationSettingsFormSet',
    # Translation
    'EnglishCreateForm',
    'EnglishUpdateForm',
]

from .case import (
    CaseRequestForm,
)
from .parameters import (
    ParametersForm,
    PresentationSettingsForm,
    PresentationSettingsFormSet,
    TranslationSettingsForm,
    TranslationSettingsFormSet,
)
from .translation import (
    EnglishCreateForm,
    EnglishUpdateForm,
)
