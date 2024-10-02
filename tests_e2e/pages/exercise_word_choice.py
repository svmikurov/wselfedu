"""The word choice for word study exercise page representation."""

from playwright.sync_api import Page

from config.constants import SUBMIT
from tests_e2e.pages.base import POMPage


class WordChoiceExercisePage(POMPage):
    """The word choice for word study exercise page representation.

    Parameters
    ----------
    page : `Page`
        Playwright page instance.

    Attributes
    ----------
    path : `str`
        It page path schema.
    timeout_input : `Locator`
        The time for question display fild input locator.
    language_order : `Locator`
        The question word language display choice locator.
    submit_button : 'Locator'
        The submit button locator.

    """

    title = 'Выбор слов для изучения'
    """The page title.
    """

    def __init__(self, page: Page) -> None:
        """Word choice exercise page constructor."""
        super().__init__(page)
        self.path = '/foreign/foreign-translate-choice'
        self.timeout_input = page.get_by_label('Время на ответ (сек)*')
        self.language_order = page.locator('#id_language_order')
        self.submit_button = page.get_by_test_id(SUBMIT)

    def choice_word(
        self,
        question_language: str,
        task_timeout: str = '1',
    ) -> None:
        """Make choice words for study.

        Parameters
        ----------
        question_language : `str`
            Choice value to display word`s language for translate.
        task_timeout : `str`, optional
            Time value to display word without translate, sec (the
            default is 1 sec).

        """
        self.timeout_input.fill(task_timeout)
        self.language_order.select_option(question_language)
        self.submit_button.click()
