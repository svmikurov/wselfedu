from english.views.home import (
    HomeEnglishView,
)
from english.views.categories import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from english.views.word_task_view import (
    AnswerWordStudyView,
    WordChoiceView,
    QuestionWordStudyView,
    start_study_word_view,
    update_words_favorites_status_view,
    update_words_knowledge_assessment_view,
)
from english.views.sources import (
    SourceCreateView,
    SourceListView,
    SourceUpdateView,
    SourceDeleteView,
)
from english.views.crud_word_view import (
    DEFAULT_CATEGORY,
    WordCreateView,
    WordListView,
    WordDetailView,
    WordUpdateView,
    WordDeleteView,
    ShowUsersWordsView,
)
from english.views.lessons import (
    LessonsListView,
    LessonCreateView,
    LessonUpdateView,
    LessonDeleteView,
)
from english.views.learn_django import (
    CalendarView,
)
