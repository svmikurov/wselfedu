"""Language discipline forms."""

__all__ = [
    # Parameters
    'ParametersForm',
    'PresentationSettingsForm',
    'PresentationSettingsFormSet',
    'TranslationSettingsForm',
    'TranslationSettingsFormSet',
    # Translation
    'EnglishCreateForm',
    'EnglishUpdateForm',
    # English language rule
    'RuleForm',
    'RuleExampleForm',
    'RuleExceptionForm',
]

from .parameters import (
    ParametersForm,
    PresentationSettingsForm,
    PresentationSettingsFormSet,
    TranslationSettingsForm,
    TranslationSettingsFormSet,
)
from .rule import (
    RuleExampleForm,
    RuleExceptionForm,
    RuleForm,
)
from .translation import (
    EnglishCreateForm,
    EnglishUpdateForm,
)
