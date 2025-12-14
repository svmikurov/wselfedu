"""Language discipline web urls paths."""

from django.urls import path

from . import views

app_name = 'lang'

urlpatterns = [
    path('', views.IndexLangView.as_view(), name='index'),
    path(
        'mark/create/',
        views.MarkCreateView.as_view(),
        name='mark_create',
    ),
    path(
        'mark/<int:pk>/update/',
        views.MarkUpdateView.as_view(),
        name='mark_update',
    ),
    path(
        'mark/<int:pk>/delete/',
        views.MarkDeleteView.as_view(),
        name='mark_delete',
    ),
    path(
        'mark/<int:pk>/',
        views.MarkDetailView.as_view(),
        name='mark_detail',
    ),
    path(
        'mark/list/',
        views.LabelListView.as_view(),
        name='mark_list',
    ),
    path(
        'translation/english/create/',
        views.EnglishTranslationCreateView.as_view(),
        name='translation_english_create',
    ),
    path(
        'translation/english/list/',
        views.EnglishTranslationListView.as_view(),
        name='translation_english_list',
    ),
    path(
        'translation/english/<int:pk>/update/',
        views.EnglishTranslationUpdateView.as_view(),
        name='translation_english_update',
    ),
    path(
        'translation/english/<int:pk>/delete/',
        views.EnglishTranslationDeleteView.as_view(),
        name='translation_english_delete',
    ),
    path(
        'translation/english/study/',
        views.EnglishTranslationStudyView.as_view(),
        name='translation_english_study',
    ),
    path(
        'translation/english/study/case/',
        views.english_translation_case_htmx_view,
        name='translation_english_study_case',
    ),
]
