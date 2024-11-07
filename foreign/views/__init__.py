"""Foreign words dictionary app views."""

# ruff: noqa: I001
from foreign.views.category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
)
from foreign.views.exercise import (
    WordExerciseView,
    WordExerciseParamsView,
    update_word_progress_view,
    update_words_favorites_status_view_ajax,
)
from foreign.views.params import (
    CreateForeignTaskSettingsView,
    ForeignTaskSettingsView,
    UpdateForeignTaskSettingsView,
)
from foreign.views.source import (
    SourceCreateView,
    SourceDeleteView,
    SourceDetailView,
    SourceListView,
    SourceUpdateView,
)
from foreign.views.word import (
    WordCreateView,
    WordDeleteView,
    WordDetailView,
    WordListView,
    WordUpdateView,
)
from foreign.views.word_list import (
    UserWordListView,
)
from foreign.views.mentorship import (
    AddWordByMentorToStudentView,
)

__all__ = [
    'AddWordByMentorToStudentView',
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryDetailView',
    'CategoryListView',
    'CategoryUpdateView',
    'CreateForeignTaskSettingsView',
    'ForeignTaskSettingsView',
    'WordExerciseView',
    'WordExerciseParamsView',
    'SourceCreateView',
    'SourceDeleteView',
    'SourceDetailView',
    'SourceListView',
    'SourceUpdateView',
    'UpdateForeignTaskSettingsView',
    'UserWordListView',
    'WordCreateView',
    'WordDeleteView',
    'WordDetailView',
    'WordListView',
    'WordUpdateView',
    'update_word_progress_view',
    'update_words_favorites_status_view_ajax',
]
