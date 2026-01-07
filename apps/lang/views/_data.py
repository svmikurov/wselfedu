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


# TODO: Move ''case_url' to service?
class PresentationViewContext(ViewContext):
    """View context with submit text."""

    case_url: str


class TranslationContext(TypedDict):
    """Translation context types."""

    create: SubmitViewContext
    update: SubmitViewContext
    list: ViewContext
    parameters: ViewContext
    english_study: PresentationViewContext
    translation_test: ViewContext


class RuleContext(TypedDict):
    """Language rule context types."""

    index: ViewContext
    list: ViewContext
    create_rule: ViewContext
    update_rule: ViewContext
    detail_rule: ViewContext


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
        'case_url': '/lang/translation/english/study/case/',
    },
    # English translation tests
    'translation_test': {
        'title': 'Словарный тест',
        'header': 'Словарный тест',
    },
}

ENGLISH_RULE: RuleContext = {
    'index': {
        'title': 'Английский язык',
        'header': 'Английский язык',
    },
    'list': {
        'title': 'Правила английского языка',
        'header': 'Правила английского языка',
    },
    'create_rule': {
        'title': 'Добавление правила английского языка',
        'header': 'Добавление правила английского языка',
    },
    'update_rule': {
        'title': 'Изменение правила английского языка',
        'header': 'Изменение правила английского языка',
    },
    'detail_rule': {
        'title': 'Правило английского языка',
        'header': 'Правило английского языка',
    },
}
