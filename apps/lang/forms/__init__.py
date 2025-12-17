"""Language discipline forms."""

__all__ = [
    'EnglishCreateForm',
    'EnglishUpdateForm',
    'ParametersForm',
    'TranslationSettingsForm',
    'PresentationSettingsForm',
    'TranslationSettingsFormSet',
    'PresentationSettingsFormSet',
]

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
