from english.views.english_views import (
    update_word_knowledge_assessment_view,
    update_words_favorites_status_view_ajax,
)
from english.views.settings_views import (
    EnglishTaskSettingsView,
    CreateEnglishTaskSettingsView,
    UpdateEnglishTaskSettingsView,
)
from english.views.user_word_list import (
    UserWordListView,
)
from english.views.crud_categories import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryDetailView,
)
from english.views.crud_word import (
    WordCreateView,
    WordListView,
    WordDetailView,
    WordUpdateView,
    WordDeleteView,
)
from english.views.crud_sources import (
    SourceCreateView,
    SourceUpdateView,
    SourceDeleteView,
    SourceListView,
    SourceDetailView
)

__all__ = [
    'update_word_knowledge_assessment_view',
    'update_words_favorites_status_view_ajax',
    'EnglishTaskSettingsView',
    'CreateEnglishTaskSettingsView',
    'UpdateEnglishTaskSettingsView',
    'UserWordListView',
    'CategoryCreateView',
    'CategoryListView',
    'CategoryUpdateView',
    'CategoryDeleteView',
    'CategoryDetailView',
    'WordCreateView',
    'WordListView',
    'WordDetailView',
    'WordUpdateView',
    'WordDeleteView',
    'SourceCreateView',
    'SourceUpdateView',
    'SourceDeleteView',
    'SourceListView',
    'SourceDetailView',
]
