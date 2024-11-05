"""Representation of sidebar for browser testing."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class SidebarComponent(POMPage):
    """Sidebar representation."""

    def __init__(self, page: Page) -> None:
        """Construct the sidebar representation."""
        super().__init__(page)
        self.page = page

        self.link_profile = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Личный кабинет')
        )  # fmt: skip
        self.link_foreign = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Иностранный язык')
        )  # fmt: skip
        self.link_foreign_exercise = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Упражнение "Изучаем слова"')
        )  # fmt: skip
        self.link_foreign_list = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Список слов')
        )  # fmt: skip
        self.link_foreign_create = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Добавить слово в словарь')
        )  # fmt: skip
        self.link_foreign_category = (
            page
            .get_by_test_id('sidebar')
            .get_by_test_id('foreign-chapters')
            .get_by_role('link', name='Категории')
        )  # fmt: skip
        self.link_foreign_source = (
            page
            .get_by_test_id('sidebar')
            .get_by_test_id('foreign-chapters')
            .get_by_role('link', name='Источники')
        )  # fmt: skip
        self.link_glossary = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Глоссарий')
        )  # fmt: skip
        self.link_glossary_exercise = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Упражнение "Изучаем термины"')
        )  # fmt: skip
        self.link_glossary_list = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Список терминов')
        )  # fmt: skip
        self.link_glossary_create = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Добавить термин')
        )  # fmt: skip
        self.link_glossary_category = (
            page
            .get_by_test_id('sidebar')
            .get_by_test_id('glossary-chapters')
            .get_by_role('link', name='Категории')
        )  # fmt: skip
        self.link_glossary_source = (
            page
            .get_by_test_id('sidebar')
            .get_by_test_id('glossary-chapters')
            .get_by_role('link', name='Источники')
        )  # fmt: skip
        self.link_math = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Математика')
        )  # fmt: skip
        self.link_math_exercise = (
            page
            .get_by_test_id('sidebar')
            .get_by_role('link', name='Упражнение "Вычисления"')
        )  # fmt: skip

    def click_link_profile(self) -> None:
        """Click profile link."""
        self.link_profile.click()

    def click_link_foreign(self) -> None:
        """Click foreign words link."""
        self.link_foreign.click()

    def click_link_foreign_exercise(self) -> None:
        """Click foreign exercise link."""
        self.link_foreign_exercise.click()

    def click_link_foreign_list(self) -> None:
        """Click foreign word list link."""
        self.link_foreign_list.click()

    def click_link_foreign_create(self) -> None:
        """Click foreign word create link."""
        self.link_foreign_create.click()

    def click_link_foreign_category(self) -> None:
        """Click foreign category link."""
        self.link_foreign_category.click()

    def click_link_foreign_source(self) -> None:
        """Click foreign source link."""
        self.link_foreign_source.click()

    def click_link_glossary(self) -> None:
        """Click glossary link."""
        self.link_glossary.click()

    def click_link_glossary_exercise(self) -> None:
        """Click glossary exercise link."""
        self.link_glossary_exercise.click()

    def click_link_glossary_list(self) -> None:
        """Click glossary list link."""
        self.link_glossary_list.click()

    def click_link_glossary_create(self) -> None:
        """Click glossary term create link."""
        self.link_glossary_create.click()

    def click_link_glossary_category(self) -> None:
        """Click glossary category link."""
        self.link_glossary_category.click()

    def click_link_glossary_source(self) -> None:
        """Click glossary source link."""
        self.link_glossary_source.click()

    def click_link_math(self) -> None:
        """Click math link."""
        self.link_math.click()

    def click_link_math_exercise(self) -> None:
        """Click math link."""
        self.link_math_exercise.click()
