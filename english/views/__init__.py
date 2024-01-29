from english.views.home import HomeEnglishView

from english.views.categories import CategoryCreateView
from english.views.categories import CategoryListView
from english.views.categories import CategoryUpdateView
from english.views.categories import CategoryDeleteView

from english.views.study_words import ChooseEnglishWordsStudyView
from english.views.study_words import study_words_view

from english.views.sources import SourceCreateView
from english.views.sources import SourceListView
from english.views.sources import SourceUpdateView
from english.views.sources import SourceDeleteView

from english.views.words import WordCreateView
from english.views.words import WordListView
from english.views.words import WordUpdateView
from english.views.words import WordDeleteView
from english.views.words import ShowUsersWordsView

from english.views.lessons import LessonsListView
from english.views.lessons import LessonCreateView
from english.views.lessons import LessonUpdateView
from english.views.lessons import LessonDeleteView

from english.views.handle_requests_db import update_words_knowledge_assessment_view
from english.views.handle_requests_db import update_words_favorites_status_view
