"""Language view context."""

from typing import TypedDict


class ViewContext(TypedDict):
    """View context types."""

    title: str
    header: str


class SubmitViewContext(ViewContext):
    """View context with submit text."""

    submit_text: str


class TranslationContext(TypedDict):
    """Translation context types."""

    create: SubmitViewContext
    update: SubmitViewContext
    list: ViewContext


TRANSLATION_CONTEXT: TranslationContext = {
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
}
