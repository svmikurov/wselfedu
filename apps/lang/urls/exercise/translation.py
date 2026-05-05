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
    # =============================================
    # GET: renders initial template with first task, JS business-logic
    # for next exercise actions
    # POST: renders partial templates with next task in exercise loop;
    # handlers other requests (update progress, explain, ...)
    path(
        'translation/english/study/',
        TranslationPresentationView.as_view(),
        name='translation_english_study',
    ),
    # =============================================
    # Translation test
    # =============================================
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
