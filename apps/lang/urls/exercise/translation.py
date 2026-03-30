"""English discipline translation exercises url paths."""

from django.urls import path
from django.views.generic import TemplateView

from apps.lang.views import (
    RegularTranslationTestPerformView,
    TranslationPresentationView,
)

urlpatterns = [
    # =============================================
    # Translation presentation
    # ---------------------------------------------
    # Renders presentation exercise template with JS business-logic to
    # display presentation, request new case and update study progress.
    path(
        'translation/english/study/',
        TranslationPresentationView.as_view(),
        name='translation_english_study',
    ),
    # Renders new presentation case.
    path(
        'translation/english/study/case/',
        TemplateView.as_view(template_name='stub.html'),
        name='translation_english_study_case',
    ),
    # =============================================
    # Translation test exercise
    # ---------------------------------------------
    # Self-education
    path(
        'translation/english/test/',
        RegularTranslationTestPerformView.as_view(),
        name='translation_english_test',
    ),
    # Mentorship
    path(
        'translation/english/test/<int:pk>/mentorship/',
        TemplateView.as_view(template_name='stub.html'),
        name='translation_english_test_mentorship',
    ),
]
