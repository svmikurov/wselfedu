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
    ForeignExerciseParamsView,
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
    WordToStudentView,
    WordToStudentView2,
)

__all__ = [
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryDetailView',
    'CategoryListView',
    'CategoryUpdateView',
    'CreateForeignTaskSettingsView',
    'ForeignExerciseParamsView',
    'ForeignTaskSettingsView',
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
    'WordExerciseView',
    'WordListView',
    'WordToStudentView',
    'WordToStudentView2',
    'WordUpdateView',
    'update_word_progress_view',
    'update_words_favorites_status_view_ajax',
]
