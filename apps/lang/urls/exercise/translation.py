"""English discipline translation exercises url paths."""

from django.urls import path

from ... import views

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
        views.TranslationTestView.as_view(),
        name='translation_english_test',
    ),
    path(
        'translation/english/test/progress/',
        views.TranslationTestProgressView.as_view(),
        name='translation_english_test_progress',
    ),
    # Mentorship
    path(
        'translation/english/test/<int:pk>/mentorship/',
        views.TranslationTestMentorshipView.as_view(),
        name='translation_english_test_mentorship',
    ),
]
