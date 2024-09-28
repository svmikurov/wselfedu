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

        # Favorites word checkbox.
        self.favorites_choice = page.get_by_label('Favorites')
        # Translate order choice.
        self.language_order_choice = page.locator('#id_language_order')
        # Word category choice.
        self.category_choice = page.locator('#id_category')
        # Word source choice.
        self.source_choice = page.locator('#id_source')
        # Word adding edge period choice.
        self.start_period_choice = page.locator('#id_period_start_date')
        self.end_period_choice = page.locator('#id_period_end_date')
        # Study progress checkboxes.
        self.study_progres_label = page.get_by_label('Изучаю')
        self.repeat_progres_label = page.get_by_label('Повторяю')
        self.repeat_progres_label = page.get_by_label('Проверяю')
        self.examination_progres_label = page.get_by_label('Знаю')
        self.study_progres_choice = page.locator('#id_knowledge_assessment_0')
        self.repeat_progres_choice = page.locator('#id_knowledge_assessment_1')
        self.examination_progres_choice = page.locator(
            '#id_knowledge_assessment_2'
        )
        self.know_progres_choice = page.locator('#id_knowledge_assessment_3')
        # Answer timeout
        self.timeout_choice = page.get_by_label('Время на ответ (сек)*')
        # Word length checkboxes.
        self.ow_length_label = page.get_by_label('Слово', exact=True)
        self.cb_length_label = page.get_by_label('Словосочетание')
        self.ps_length_label = page.get_by_label('Часть предложения')
        self.st_length_label = page.get_by_label('Предложение')
        self.ow_length_choice = page.locator('#id_word_count_0')
        self.cb_length_choice = page.locator('#id_word_count_1')
        self.ps_length_choice = page.locator('#id_word_count_2')
        self.st_length_choice = page.locator('#id_word_count_3')
