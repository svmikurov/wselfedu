"""Language discipline views."""

__all__ = [
    'IndexLangView',
    'MarkCreateView',
    'MarkUpdateView',
    'MarkDeleteView',
    'MarkDetailView',
    'LabelListView',
    'EnglishTranslationCreateView',
    'EnglishTranslationListView',
    'EnglishTranslationUpdateView',
    'EnglishTranslationDeleteView',
    'study_settings_vew',
    # Study
    'EnglishTranslationStudyView',
    'EnglishTranslationStudyCaseView',
    # Test
    'TranslationTestView',
    'TranslationTestProgressView',
    'TranslationTestMentorshipView',
    # Rule
    'RuleIndexView',
    'RuleListView',
    'RuleDetailView',
    'RuleCreateView',
    'RuleUpdateView',
    'RuleDeleteView',
    'RuleExampleView',
    'RuleExceptionView',
    # Rule for mentorship
    'RuleStudentView',
    'RuleStudentListView',
    'RuleMentorListView',
]

from .index import IndexLangView
from .label import (
    LabelListView,
    MarkCreateView,
    MarkDeleteView,
    MarkDetailView,
    MarkUpdateView,
)
from .presentation import (
    EnglishTranslationStudyCaseView,
    EnglishTranslationStudyView,
)
from .rule import (
    RuleExampleView,
    RuleExceptionView,
    RuleDetailView,
    RuleCreateView,
    RuleDeleteView,
    RuleIndexView,
    RuleListView,
    RuleUpdateView,
    RuleStudentView,
    RuleStudentListView,
    RuleMentorListView,
)
from .settings import (
    study_settings_vew,
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
