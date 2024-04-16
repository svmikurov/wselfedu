from django.urls import path

from english import views

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
        views.WordListView.as_view(),
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
    path(
        'words-favorites-view-ajax/<int:word_id>/',
        views.update_words_favorites_status_view_ajax,
        name='word_favorites_view_ajax',
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
        name='category_list'
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
    path(
        'categories/<int:pk>/detail/',
        views.CategoryDetailView.as_view(),
        name='categories_detail'
    ),
    # --======= Sources =======--
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
    path(
        'sources/list/',
        views.SourceListView.as_view(),
        name='source_list'
    ),
    path(
        'sources/<int:pk>/detail/',
        views.SourceDetailView.as_view(),
        name='source_detail'
    ),
    # --======= Analysis =======--
    path(
        '<int:pk>/word-information/',
        views.AnalysisWordUserView.as_view(),
        name='word_information'
    ),
]
