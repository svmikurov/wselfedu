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
    # Rule
    'ClauseForm',
    'ClauseExampleForm',
    'RuleForm',
    'RuleExceptionForm',
    'ClauseTranslationForm',
    # Mentorship
    'RuleAssignmentForm',
]

from .parameters import (
    ParametersForm,
    PresentationSettingsForm,
    PresentationSettingsFormSet,
    TranslationSettingsForm,
    TranslationSettingsFormSet,
)
from .rule import (
    ClauseExampleForm,
    ClauseForm,
    RuleAssignmentForm,
    RuleExceptionForm,
    RuleForm,
    ClauseTranslationForm,
)
from .translation import (
    EnglishCreateForm,
    EnglishUpdateForm,
)
