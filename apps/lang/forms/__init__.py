"""Language discipline forms."""

__all__ = [
    # Case
    'CaseParametersForm',
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
    CaseParametersForm,
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
