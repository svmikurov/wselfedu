"""English exercise conditions choice page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class EnglishExerciseConditionsChoicePage(POMPage):
    """English exercise conditions choice test page."""

    title = 'Выбор слов для изучения'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.page = page
        self.path = '/task/english-translate-choice/'

        self.favorites_choice = page.get_by_label('Favorites')
        self.language_order_choice = page.locator('#id_language_order')
        self.category_choice = page.locator('#id_category')
        self.source_choice = page.locator('#id_source')
        self.start_period_choice = page.locator('#id_period_start_date')
        self.end_period_choice = page.locator('#id_period_end_date')
        self.study_progres_choice = page.locator('#id_knowledge_assessment_0')
        self.repeat_progres_choice = page.locator('#id_knowledge_assessment_1')
        self.examination_progres_choice = page.locator(
            '#id_knowledge_assessment_2'
        )
        self.know_progres_choice = page.locator('#id_knowledge_assessment_3')
        self.timeout_choice = page.get_by_label('Время на ответ (сек)*')
        self.ow_length_choice = page.get_by_label('Слово')
        self.cb_length_choice = page.get_by_label('Словосочетание')
        self.ps_length_choice = page.get_by_label('Часть предложения')
        self.st_length_choice = page.get_by_label('Предложение')
