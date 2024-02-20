from django.urls import path

from english import views


study = [
    # --======= Calendar ========--
    path(
        'calendar/',
        views.CalendarView.as_view(),
        name='calendar',
    ),
    # -- End Calendar --
    # --======= SQL =======--
]


app_name = 'english'
urlpatterns = [
    # --======= English chapter =======--
    path(
        # Show list of registrations users.
        '',
        views.HomeEnglishView.as_view(),
        name='home',
    ),
    # --======= Account ======--
    path(
        'user/<int:pk>/word-list/',
        views.UsersWordsView.as_view(),
        name='users_words',
    ),
    # -- End Account --
    # --======= Task word study =======--
    # Отображение параметров для выборки слов на задание.
    path(
        'words-choice/',
        views.WordChoiceView.as_view(),
        name='word_choice',
    ),
    # Сохранение параметров выборки слов для задания.
    path(
        'words-start/',
        views.start_study_word_view,
        name='start_word_study',
    ),
    # Отображение вопроса.
    path(
        'word-study/question/',
        views.QuestionWordStudyView.as_view(),
        name='word_study_question',
    ),
    # Отображение ответа.
    path(
        'word-study/answer/',
        views.AnswerWordStudyView.as_view(),
        name='word_study_answer',
    ),
    # Добавление оценки слова.
    path(
        'knowledge-assessment/<int:word_id>/',
        views.update_words_knowledge_assessment_view,
        name='knowledge_assessment'
    ),
    # Изменение статуса избранного слова.
    path(
        'words-favorites-view/<int:word_id>/<str:from_page>/',
        views.update_words_favorites_status_view,
        name='word_favorites_view',
    ),
    # -- End Task study words --

    # --======= Word =======--
    path(
        'word/list/',
        views.WordListView.as_view(),
        name='word_list',
    ),
    path(
        'word/create/',
        views.WordCreateView.as_view(),
        name='words_create',
    ),
    path('word/<int:pk>/detail/',
         views.WordDetailView.as_view(),
         name='words_detail'
         ),
    path(
        'word/<int:pk>/update/',
        views.WordUpdateView.as_view(),
        name='words_update',
    ),
    path(
        'word/<int:pk>/delete/',
        views.WordDeleteView.as_view(),
        name='words_delete',
    ),

    # --======= Categories =======--
    path(
        'categories/list/',
        views.CategoryListView.as_view(),
        name='categories_list'
    ),
    path(
        'categories/create/',
        views.CategoryCreateView.as_view(),
        name='categories_create'
    ),
    path(
        'categories/<int:pk>/update/',
        views.CategoryUpdateView.as_view(),
        name='categories_update'
    ),
    path(
        'categories/<int:pk>/delete/',
        views.CategoryDeleteView.as_view(),
        name='categories_delete'
    ),

    # --======= Sources =======--
    path(
        'sources/list/',
        views.SourceListView.as_view(),
        name='sources_list'
    ),
    path(
        'sources/create/',
        views.SourceCreateView.as_view(),
        name='source_create'
    ),
    path(
        'sources/<int:pk>/update/',
        views.SourceUpdateView.as_view(),
        name='source_update'
    ),
    path(
        'sources/<int:pk>/delete/',
        views.SourceDeleteView.as_view(),
        name='source_delete'
    ),

    # --======= Lessons =======--
    path(
        'lessons/list/',
        views.LessonsListView.as_view(),
        name='lessons_list'
    ),
    path(
        'lessons/create/',
        views.LessonCreateView.as_view(),
        name='lesson_create'
    ),
    path(
        'lessons/<int:pk>/update/',
        views.LessonUpdateView.as_view(),
        name='lesson_update'
    ),
    path(
        'lessons/<int:pk>/delete/',
        views.LessonDeleteView.as_view(),
        name='lesson_delete'
    ),
] + study
