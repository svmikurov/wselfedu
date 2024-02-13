from english.views.home import (
    HomeEnglishView,
)
from english.views.categories import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from english.views.word_study import (
    AnswerWordStudyView,
    ChooseEnglishWordsStudyView,
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
from english.views.words import (
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
