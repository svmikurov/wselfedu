"""Language discipline views."""

__all__ = [
    'IndexLangView',
    'MarkCreateView',
    'MarkUpdateView',
    'MarkDeleteView',
    'MarkListView',
    'EnglishTranslationCreateView',
    'EnglishTranslationListView',
    'EnglishTranslationUpdateView',
    'EnglishTranslationDeleteView',
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

from .index import IndexLangView
from .mark import (
    MarkCreateView,
    MarkDeleteView,
    MarkListView,
    MarkUpdateView,
)
from .presentation import (
    EnglishTranslationStudyCaseView,
    EnglishTranslationStudyView,
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
from .settings import (
    study_settings_view,
)
from .translation import (
    EnglishTranslationCreateView,
    EnglishTranslationDeleteView,
    EnglishTranslationListView,
    EnglishTranslationUpdateView,
)
from .translation_test import (
    TranslationTestMentorshipView,
    TranslationTestProgressView,
    TranslationTestView,
)
