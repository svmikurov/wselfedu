"""Learning foreign words exercise conditions choice page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignExerciseParamsPage(POMPage):
    """Foreign exercise conditions choice test page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Выбор слов для изучения'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.path = '/foreign/foreign-translate-choice/'

        # Favorites word checkbox.
        self.favorites_choice = page.get_by_label('Только избранные слова')
        # Translate order choice.
        self.order_choice = page.locator('#id_order')
        # Word category choice.
        self.category_choice = page.locator('#id_category')
        # Word source choice.
        self.source_choice = page.locator('#id_source')
        # Word adding edge period choice.
        self.start_period_choice = page.locator('#id_period_start_date')
        self.end_period_choice = page.locator('#id_period_end_date')
        # Study progress checkboxes.
        self.study_progress_label = page.get_by_label('Изучаю')
        self.repeat_progress_label = page.get_by_label('Повторяю')
        self.repeat_progress_label = page.get_by_label('Проверяю')
        self.examination_progress_label = page.get_by_label('Знаю')
        self.study_progress_choice = page.locator('#id_progress_0')
        self.repeat_progress_choice = page.locator('#id_progress_1')
        self.examination_progress_choice = page.locator('#id_progress_2')
        self.know_progress_choice = page.locator('#id_progress_3')
        # Answer timeout
        self.timeout_choice = page.get_by_label('Время на ответ (сек)*')
        # Word length checkboxes.
        self.ow_length_label = page.get_by_label('Слово', exact=True)
        self.cb_length_label = page.get_by_label('Словосочетание')
        self.ps_length_label = page.get_by_label('Часть предложения')
        self.st_length_label = page.get_by_label('Предложение')
