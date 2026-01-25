"""English discipline translation exercises url paths."""

from django.urls import path

from ... import views
from ...views.exercise.test import progress, translation

urlpatterns = [
    # ------------
    # Presentation
    # ------------
    path(
        'translation/english/study/',
        views.EnglishTranslationStudyView.as_view(),
        name='translation_english_study',
    ),
    path(
        'translation/english/study/case/',
        views.EnglishTranslationStudyCaseView.as_view(),
        name='translation_english_study_case',
    ),
    # ----
    # Test
    # ----
    # Self-education
    path(
        'translation/english/test/',
        translation.TranslationTestView.as_view(),
        name='translation_english_test',
    ),
    # REVIEW: Replace progress path definition?
    path(
        'translation/english/test/progress/',
        progress.TranslationTestProgressView.as_view(),
        name='translation_english_test_progress',
    ),
    # Mentorship
    path(
        'translation/english/test/<int:pk>/mentorship/',
        translation.TranslationTestMentorshipView.as_view(),
        name='translation_english_test_mentorship',
    ),
]
