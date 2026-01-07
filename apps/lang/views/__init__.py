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
    # Language rule views
    'EnglishRuleIndexView',
    'EnglishRuleListView',
    'EnglishRuleCreateView',
    'EnglishRuleUpdateView',
    'EnglishRuleDeleteView',
    'EnglishRuleDetailView',
    'EnglishRuleStudentView',
    # mentorship
    'EnglishRuleStudentListView',
    'EnglishRuleMentorListView',
    # rule clause edit example
    'EditRuleClauseExampleView',
    'EditRuleExceptionView',
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
    EditRuleClauseExampleView,
    EditRuleExceptionView,
    EnglishRuleCreateView,
    EnglishRuleDeleteView,
    EnglishRuleDetailView,
    EnglishRuleIndexView,
    EnglishRuleListView,
    EnglishRuleMentorListView,
    EnglishRuleStudentListView,
    EnglishRuleUpdateView,
    EnglishRuleStudentView,
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
