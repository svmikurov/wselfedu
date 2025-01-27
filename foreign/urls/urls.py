"""Foreign word urls."""

from django.urls import path
from django.views.generic import TemplateView

from foreign import views
from foreign.views import (
    ForeignExerciseParamsView,
    WordExerciseView,
    update_word_progress_view,
)

app_name = 'foreign'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='foreign/main.html'),
        name='main',
    ),
]

word_paths = [
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
    path(
        'word/<int:pk>/detail/',
        views.WordDetailView.as_view(),
        name='words_detail',
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
]

category_paths = [
    path(
        'categories/list/',
        views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'categories/create/',
        views.CategoryCreateView.as_view(),
        name='categories_create',
    ),
    path(
        'categories/<int:pk>/update/',
        views.CategoryUpdateView.as_view(),
        name='categories_update',
    ),
    path(
        'categories/<int:pk>/delete/',
        views.CategoryDeleteView.as_view(),
        name='categories_delete',
    ),
    path(
        'categories/<int:pk>/detail/',
        views.CategoryDetailView.as_view(),
        name='categories_detail',
    ),
]

source_paths = [
    path(
        'sources/create/',
        views.SourceCreateView.as_view(),
        name='source_create',
    ),
    path(
        'sources/<int:pk>/update/',
        views.SourceUpdateView.as_view(),
        name='source_update',
    ),
    path(
        'sources/<int:pk>/delete/',
        views.SourceDeleteView.as_view(),
        name='source_delete',
    ),
    path(
        'sources/list/',
        views.SourceListView.as_view(),
        name='source_list',
    ),
    path(
        'sources/<int:pk>/detail/',
        views.SourceDetailView.as_view(),
        name='source_detail',
    ),
]

mentorship_paths = [
    path(
        'word-to-student/<int:student_id>/',
        views.WordToStudentView.as_view(),
        name='word_to_student',
    ),
    path(
        'word-to-student2/<int:student_id>/',
        views.WordToStudentView2.as_view(),
        name='word_to_student2',
    ),
]

exercise_paths = [
    path(
        'foreign-translate-choice/',
        ForeignExerciseParamsView.as_view(),
        name='params',
    ),
    path(
        'foreign-translate-demo/',
        WordExerciseView.as_view(),
        name='foreign_translate_demo',
    ),
    path(
        'progress/<int:word_id>/',
        update_word_progress_view,
        name='progress',
    ),
    path(
        '<int:pk>/create-task-settings/',
        views.CreateForeignTaskSettingsView.as_view(),
        name='create_task_settings',
    ),
    path(
        '<int:pk>/update-task-settings/',
        views.UpdateForeignTaskSettingsView.as_view(),
        name='update_task_settings',
    ),
    path(
        'words-favorites-view-ajax/<int:word_id>/',
        views.update_words_favorites_status_view_ajax,
        name='word_favorites_view_ajax',
    ),
]

urlpatterns += word_paths
urlpatterns += category_paths
urlpatterns += source_paths
urlpatterns += mentorship_paths
urlpatterns += exercise_paths
