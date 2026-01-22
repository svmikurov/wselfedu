"""Language discipline views."""

__all__ = [
    'study_settings_view',
    # Study
    'EnglishTranslationStudyView',
    'EnglishTranslationStudyCaseView',
    # Test
    'TranslationTestView',
    'TranslationTestProgressView',
    'TranslationTestMentorshipView',
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
]

from .exercise.presentation.translation import (
    EnglishTranslationStudyCaseView,
    EnglishTranslationStudyView,
)
from .exercise.settings import (
    study_settings_view,
)
from .exercise.test.translation import (
    TranslationTestMentorshipView,
    TranslationTestProgressView,
    TranslationTestView,
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
