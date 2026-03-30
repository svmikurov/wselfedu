"""Language discipline views."""

__all__ = [
    'study_settings_view',
    # Rule
    'RuleView',
    'RuleListView',
    'RuleDetailView',
    'RuleCreateView',
    'RuleUpdateView',
    'RuleDeleteView',
    'ClauseCreateView',
    'WordExampleAddView',
    'ExceptionAddView',
    'TaskExampleAddView',
    'WordExampleListView',
    # Mentorship
    'RuleAssignmentCreate',
    'ClauseUpdateView',
    # Exercise
    'TranslationPresentationView',
    'RegularTranslationTestPerformView',
]

from .exercise.settings import (
    study_settings_view,
)
from .exercise.translation.presentation import (
    TranslationPresentationView,
)
from .exercise.translation.test import (
    RegularTranslationTestPerformView,
)
from .rule import (
    ClauseCreateView,
    ClauseUpdateView,
    ExceptionAddView,
    RuleAssignmentCreate,
    RuleCreateView,
    RuleDeleteView,
    RuleDetailView,
    RuleListView,
    RuleUpdateView,
    RuleView,
    TaskExampleAddView,
    WordExampleAddView,
    WordExampleListView,
)
