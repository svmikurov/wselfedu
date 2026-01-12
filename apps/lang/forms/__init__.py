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
    'TaskExampleForm',
    'RuleForm',
    'RuleExceptionForm',
    'WordExampleForm',
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
    ClauseForm,
    RuleAssignmentForm,
    RuleExceptionForm,
    RuleForm,
    TaskExampleForm,
    WordExampleForm,
)
from .translation import (
    EnglishCreateForm,
    EnglishUpdateForm,
)
