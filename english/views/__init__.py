# Temp studding views.
from english.views.account_views import (
    UserWordListView,
)
from english.views.learn_django import (
    CalendarView,
)

# Basic views.
from english.views.home import (
    HomeEnglishView,
)
from english.views.crud_categories import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,
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
    SourceListView,
    SourceUpdateView,
    SourceDeleteView,
)
from english.views.word_task_view import (
    AnswerWordStudyView,
    WordChoiceView,
    QuestionWordStudyView,
    start_study_word_view,
    update_words_favorites_status_view,
    update_words_knowledge_assessment_view,
)
