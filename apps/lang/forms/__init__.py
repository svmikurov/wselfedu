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
    'AssignTranslationForm',
    'LangExerciseForm',
    'ExerciseAssignationForm',
    # Meta
    'MarkForm',
    'CategoryForm',
]

from .assignment import (
    AssignTranslationForm,
)
from .category import CategoryForm
from .exercise import (
    ExerciseAssignationForm,
    LangExerciseForm,
)
from .mark import MarkForm
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
