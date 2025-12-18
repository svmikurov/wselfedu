"""Language discipline view context data."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    pass


class ViewContext(TypedDict):
    """View context types."""

    title: str
    header: str


class SubmitViewContext(ViewContext):
    """View context with submit text."""

    submit_text: str


class PresentationViewContext(ViewContext):
    """View context with submit text."""


class TranslationContext(TypedDict):
    """Translation context types."""

    create: SubmitViewContext
    update: SubmitViewContext
    list: ViewContext
    parameters: ViewContext
    english_study: PresentationViewContext


ENGLISH_TRANSLATION: TranslationContext = {
    'create': {
        'title': 'Добавление перевода',
        'header': 'Добавление перевода',
        'submit_text': 'Добавить',
    },
    'update': {
        'title': 'Изменение перевода',
        'header': 'Изменение перевода',
        'submit_text': 'Изменить',
    },
    'list': {
        'title': 'Список переводов',
        'header': 'Список переводов',
    },
    'parameters': {
        'title': 'Настройки изучения слов',
        'header': 'Настройки изучения слов',
    },
    'english_study': {
        'title': 'Изучение английских слов',
        'header': 'Изучение английских слов',
    },
}
