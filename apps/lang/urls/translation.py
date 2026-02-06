"""English language translation CRUD url paths."""

from django.urls import path

from ..views import translation

urlpatterns = [
    path(
        'english/translation/index/',
        translation.EnglishTranslationIndexView.as_view(),
        name='english_translation_index',
    ),
    path(
        'english/translation/list/',
        translation.EnglishTranslationListView.as_view(),
        name='english_translation_list',
    ),
    path(
        'english/translation/create/',
        translation.EnglishTranslationCreateView.as_view(),
        name='english_translation_create',
    ),
    path(
        'english/translation/<int:pk>/update/',
        translation.EnglishTranslationUpdateView.as_view(),
        name='english_translation_update',
    ),
    path(
        'english/translation/<int:pk>/delete/',
        translation.EnglishTranslationDeleteView.as_view(),
        name='english_translation_delete',
    ),
]
