"""Foreign words dictionary app views."""

# ruff: noqa: I001
from english.views.crud_categories import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
)
from english.views.crud_sources import (
    SourceCreateView,
    SourceDeleteView,
    SourceDetailView,
    SourceListView,
    SourceUpdateView,
)
from english.views.crud_word import (
    WordCreateView,
    WordDeleteView,
    WordDetailView,
    WordListView,
    WordUpdateView,
)
from english.views.english_views import (
    update_word_progress_view,
    update_words_favorites_status_view_ajax,
)
from english.views.settings_views import (
    CreateForeignTaskSettingsView,
    ForeignTaskSettingsView,
    UpdateForeignTaskSettingsView,
)
from english.views.user_word_list import (
    UserWordListView,
)
from english.views.mentorship_views import (
    AddWordByMentorToStudentView,
)

__all__ = [
    'update_word_progress_view',
    'update_words_favorites_status_view_ajax',
    'ForeignTaskSettingsView',
    'CreateForeignTaskSettingsView',
    'UpdateForeignTaskSettingsView',
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
    'AddWordByMentorToStudentView',
]
