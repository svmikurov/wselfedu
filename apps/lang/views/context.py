"""Language view context."""

from typing import Any, TypedDict


class ViewContext(TypedDict):
    """View context types."""

    title: str
    header: str


class SubmitViewContext(ViewContext):
    """View context with submit text."""

    submit_text: str


class PresentationViewContext(ViewContext):
    """View context with submit text."""

    task: dict[str, Any]


class TranslationContext(TypedDict):
    """Translation context types."""

    create: SubmitViewContext
    update: SubmitViewContext
    list: ViewContext
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
    'english_study': {
        'title': 'Изучение английских слов',
        'header': 'Изучение английских слов',
        'task': {
            'task_path': '/lang/translation/english/study/case/',
        },
    },
}
