"""Representation of sidebar for browser testing."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class SidebarComponent(POMPage):
    """Sidebar representation."""

    def __init__(self, page: Page) -> None:
        """Construct the sidebar representation."""
        super().__init__(page)
        self.page = page

        sidebar = page.get_by_test_id('sidebar')
        user_chapters = sidebar.get_by_test_id('user-chapters')
        about_chapters = sidebar.get_by_test_id('about-chapters')
        foreign_chapters = sidebar.get_by_test_id('foreign-chapters')
        glossary_chapters = sidebar.get_by_test_id('glossary-chapters')
        mathematics_chapters = sidebar.get_by_test_id('mathematics-chapters')

        # User chapters.
        self.link_profile = user_chapters.get_by_role(
            'link', name='Личный кабинет',
        )  # fmt: skip
        # About chapters.
        self.link_about = about_chapters.get_by_role(
            'link', name='О проекте',
        )  # fmt: skip
        self.link_mobile = about_chapters.get_by_role(
            'link', name='Мобильное приложение',
        )  # fmt: skip
        # Foreign chapters.
        self.link_foreign_main = foreign_chapters.get_by_role(
            'link', name='Иностранный язык',
        )  # fmt: skip
        self.link_foreign_exercise = foreign_chapters.get_by_role(
            'link', name='Упражнение "Изучаем слова"',
        )  # fmt: skip
        self.link_foreign_list = foreign_chapters.get_by_role(
            'link', name='Список слов',
        )  # fmt: skip
        self.link_foreign_create = foreign_chapters.get_by_role(
            'link', name='Добавить слово в словарь',
        )  # fmt: skip
        self.link_foreign_category = foreign_chapters.get_by_role(
            'link', name='Категории',
        )  # fmt: skip
        self.link_foreign_source = foreign_chapters.get_by_role(
            'link', name='Источники',
        )  # fmt: skip
        # Glossary chapters.
        self.link_glossary_main = glossary_chapters.get_by_role(
            'link', name='Глоссарий',
        )  # fmt: skip
        self.link_glossary_exercise = glossary_chapters.get_by_role(
            'link', name='Упражнение "Изучаем термины"',
        )  # fmt: skip
        self.link_glossary_list = glossary_chapters.get_by_role(
            'link', name='Список терминов',
        )  # fmt: skip
        self.link_glossary_create = glossary_chapters.get_by_role(
            'link', name='Добавить термин',
        )  # fmt: skip
        self.link_glossary_category = glossary_chapters.get_by_role(
            'link', name='Категории',
        )  # fmt: skip
        self.link_glossary_source = glossary_chapters.get_by_role(
            'link', name='Источники',
        )  # fmt: skip
        # Mathematics chapters.
        self.link_mathematics_main = mathematics_chapters.get_by_role(
            'link', name='Математика',
        )  # fmt: skip
        self.link_math_exercise = mathematics_chapters.get_by_role(
            'link', name='Упражнение "Вычисления"',
        )  # fmt: skip

    def click_link_profile(self) -> None:
        """Click profile link."""
        self.link_profile.click()

    def click_link_about(self) -> None:
        """Click about link."""
        self.link_about.click()

    def click_link_mobile(self) -> None:
        """Click mobile link."""
        self.link_mobile.click()

    def click_link_foreign_main(self) -> None:
        """Click foreign main link."""
        self.link_foreign_main.click()

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
        """Click foreign word category link."""
        self.link_foreign_category.click()

    def click_link_foreign_source(self) -> None:
        """Click foreign word source link."""
        self.link_foreign_source.click()

    def click_link_glossary_main(self) -> None:
        """Click glossary main link."""
        self.link_glossary_main.click()

    def click_link_glossary_exercise(self) -> None:
        """Click glossary exercise link."""
        self.link_glossary_exercise.click()

    def click_link_glossary_list(self) -> None:
        """Click glossary term list link."""
        self.link_glossary_list.click()

    def click_link_glossary_create(self) -> None:
        """Click glossary term create link."""
        self.link_glossary_create.click()

    def click_link_glossary_category(self) -> None:
        """Click glossary term category link."""
        self.link_glossary_category.click()

    def click_link_glossary_source(self) -> None:
        """Click glossary term source link."""
        self.link_glossary_source.click()

    def click_link_math_main(self) -> None:
        """Click mathematics link."""
        self.link_mathematics_main.click()

    def click_link_math_exercise(self) -> None:
        """Click mathematics exercise link."""
        self.link_math_exercise.click()
