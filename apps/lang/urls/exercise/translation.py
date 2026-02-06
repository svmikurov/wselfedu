"""English discipline translation exercises url paths."""

from django.urls import path

from ... import views
from ...views.exercise.test import translation

urlpatterns = [
    # ------------
    # Presentation
    # ------------
    # Renders presentation exercise template with JS business-logic to
    # display presentation, request new case and update study progress.
    path(
        'translation/english/study/',
        views.EnglishTranslationStudyView.as_view(),
        name='translation_english_study',
    ),
    # Renders new presentation case.
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
    # Mentorship
    path(
        'translation/english/test/<int:pk>/mentorship/',
        translation.TranslationTestMentorshipView.as_view(),
        name='translation_english_test_mentorship',
    ),
]
