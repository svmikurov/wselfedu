"""The word study exercise page representation module."""

from playwright.sync_api import Page

from tests.tests_e2e.pages.base import POMPage


class WordStudyExercisePage(POMPage):
    """The word study exercise page representation class.

    Parameters
    ----------
    page : `Page`
        Playwright page instance.

    Attributes
    ----------
    path : `str`
        The page path schema.
    question_locator : `Locator`
        The question word display locator.
    answer_locator : `Locator`
        The answer word display locator.
    next_button : `Locator`
        The next exersice step button locator.
    know_button : `Locator`
        The "Know" button locator.
    not_know_button : `Locator`
        The "Don`t know" button locator.
    add_to_favorite_button : `Locator`
        The "Add to favorite" button locator.
    remove_from_favorite_button : `Locator`
        The "Remove from favorite" button locator.
    word_knowledge_indicator : `Locator`
        The word knowledge assessment value locator.

    """

    title = 'Учим слова'
    """Page title.
    """

    def __init__(self, page: Page) -> None:
        """Word study exercise page constructor."""
        super().__init__(page)
        self.path = '/task/english-translate-demo'
        self.question_locator = page.get_by_text('Вопрос:')
        self.answer_locator = page.get_by_text('Ответ:')
        self.pause_button = page.get_by_role('button', name='Пауза')
        self.next_button = page.get_by_role('button', name='Далее')
        self.know_button = page.get_by_role('button', name='Знаю', exact=True)
        self.not_know_button = page.get_by_role('button', name='Не знаю')
        self.add_to_favorite_button = self.page.get_by_text(
            'Добавить в избранные',
        )
        self.remove_from_favorite_button = self.page.get_by_text(
            'Убрать из избранных',
        )
        self.word_knowledge_indicator = self.page.get_by_text('Уровень:')
