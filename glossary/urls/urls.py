"""Glossary app DRF urls."""

from django.urls import path
from django.views.generic import TemplateView

from glossary import views
from glossary.views import GlossaryParamsView

app_name = 'glossary'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='glossary/main.html'),
        name='main',
    ),
    path(
        'term-create/',
        views.TermCreateView.as_view(),
        name='term_create',
    ),
    path(
        'term-list/',
        views.TermListView.as_view(),
        name='term_list',
    ),
    path(
        'term-detail/<int:pk>/',
        views.TermDetailView.as_view(),
        name='term_detail',
    ),
    path(
        'term-update/<int:pk>/',
        views.TermUpdateView.as_view(),
        name='term_update',
    ),
    path(
        'term-delete/<int:pk>/',
        views.TermDeleteView.as_view(),
        name='term_delete',
    ),
]

exercise_paths = [
    path(
        'params/',
        GlossaryParamsView.as_view(),
        name='params',
    ),
    path(
        'exercise/',
        views.TermExerciseView.as_view(),
        name='exercise',
    ),
    path(
        'terms-favorites-view-ajax/<int:term_id>/',
        views.update_term_favorite_status_view_ajax,
        name='term_favorites_view_ajax',
    ),
    path(
        'progress/<int:term_id>/',
        views.update_term_study_progress,
        name='progress',
    ),
]

category_paths = [
    path(
        'category/create',
        views.CategoryCreateView.as_view(),
        name='category_create',
    ),
    path(
        'category/list',
        views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'category/update/<int:pk>/',
        views.CategoryUpdateView.as_view(),
        name='category_update',
    ),
    path(
        'category/delete/<int:pk>/',
        views.CategoryDeleteView.as_view(),
        name='category_delete',
    ),
]

source_paths = [
    path(
        'create/',
        views.SourceCreateView.as_view(),
        name='source_create',
    ),
    path(
        'source/list/',
        views.SourceListView.as_view(),
        name='source_list',
    ),
    path(
        'source/update/<int:pk>/',
        views.SourceUpdateView.as_view(),
        name='source_update',
    ),
    path(
        'source/delete/<int:pk>/',
        views.SourceDeleteView.as_view(),
        name='source_delete',
    ),
]

urlpatterns += exercise_paths
urlpatterns += category_paths
urlpatterns += source_paths
