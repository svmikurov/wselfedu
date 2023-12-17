from django.urls import path

from english import views

app_name = 'eng'
urlpatterns = [
    path(
        '',
        views.HomeEnglishView.as_view(template_name='table_of_contents.html'),
        name='home',
    ),
    path(
        'repetition/',
        views.StartRepetitionWordsView.as_view(template_name='eng/tasks/start_repetition.html'),
        name='start_repetition',
    ),
    path(
        'repetition/<str:task_status>/',
        views.RepetitionWordsView.as_view(),
        name='repetition',
    ),
    path(
        'test/',
        views.TestWordView.as_view(),
        name='test',
    ),

    # --======= Words =======--
    path(
        'words/list/',
        views.WordListView.as_view(),
        name='word_list',
    ),
    path(
        'words/create/',
        views.WordCreateView.as_view(),
        name='word_create',
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
        name='sources_create'
    ),
    path(
        'sources/<int:pk>/update/',
        views.SourceUpdateView.as_view(),
        name='sources_update'
    ),
    path(
        'sources/<int:pk>/delete/',
        views.SourceDeleteView.as_view(),
        name='sources_delete'
    ),
]
