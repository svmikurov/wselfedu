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
    # For account.
    path(
        'words-users/<int:pk>/',
        views.ShowUsersWordsView.as_view(),
        name='users_words',
    ),
    # End For account.
    # --======= Tasks =======--
    path(
        'words-choose/',
        views.ChooseEnglishWordsStudyView.as_view(),
        name='words_choose',
    ),
    path(
        'words_study/<str:task_status>/',
        views.study_english_words_view,
        name='words_study',
    ),
    path(
        'test/',
        views.TestWordView.as_view(),
        name='test',
    ),
    # -- End Tasks --
    # Handle post requests to the database.
    path(
        'knowledge-assessment/<int:word_id>/',
        views.update_words_knowledge_assessment_view,
        name='knowledge_assessment'
    ),
    path(
        'words_favorites_view/<int:word_id>/',
        views.update_words_favorites_status_view,
        name='words_favorites_view',
    ),
    # End Handle post requests to the database.

    # --======= Words =======--
    path(
        'words/list/',
        views.WordListView.as_view(),
        name='words_list',
    ),
    path(
        'words/create/',
        views.WordCreateView.as_view(),
        name='words_create',
    ),
    path(
        'words/<int:pk>/update/',
        views.WordUpdateView.as_view(),
        name='words_update',
    ),
    path(
        'words/<int:pk>/delete/',
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
]
