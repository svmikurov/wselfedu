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
    'EnglishTranslationStudyView',
    'english_translation_case_htmx_view',
    'study_settings_vew',
]

from .index import IndexLangView
from .label import (
    LabelListView,
    MarkCreateView,
    MarkDeleteView,
    MarkDetailView,
    MarkUpdateView,
)
from .settings import (
    study_settings_vew,
)
from .study import (
    EnglishTranslationStudyView,
    english_translation_case_htmx_view,
)
from .translation import (
    EnglishTranslationCreateView,
    EnglishTranslationDeleteView,
    EnglishTranslationListView,
    EnglishTranslationUpdateView,
)
