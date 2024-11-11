"""Navigation links."""

from playwright.sync_api import Locator, Page

from tests_plw.pages.base import POMPage


class MainLink(POMPage):
    """Main navigation links."""

    def __init__(self, page: Page, selector: str) -> None:
        """Construct the links."""
        super().__init__(page)
        locator = self.page.locator(selector)

        self.link_profile = locator.get_by_role(
            'link', name='Личный кабинет',
        )  # fmt: skip
        self.link_home = locator.get_by_role(
            'link', name='На главную',
        )  # fmt: skip
        self.link_about = locator.get_by_role(
            'link', name='О проекте',
        )  # fmt: skip
        self.link_mobile = locator.get_by_role(
            'link', name='Мобильное приложение',
        )  # fmt: skip

    def click_link_home(self) -> None:
        """Click home link."""
        self.link_home.click()

    def click_link_profile(self) -> None:
        """Click profile link."""
        self.link_profile.click()

    def click_link_about(self) -> None:
        """Click about link."""
        self.link_about.click()

    def click_link_mobile(self) -> None:
        """Click mobile link."""
        self.link_mobile.click()


class ClickLinkMixin:
    """Click the link.

    Common mixin for ForeignLink and GlossaryLink classes.
    """

    link_main: Locator
    link_exercise: Locator
    link_list: Locator
    link_create: Locator
    link_category: Locator
    link_source: Locator

    def click_link_main(self) -> None:
        """Click main link."""
        self.link_main.click()

    def click_link_exercise(self) -> None:
        """Click exercise link."""
        self.link_exercise.click()

    def click_link_list(self) -> None:
        """Click list link."""
        self.link_list.click()

    def click_link_create(self) -> None:
        """Click create link."""
        self.link_create.click()

    def click_link_category(self) -> None:
        """Click category link."""
        self.link_category.click()

    def click_link_source(self) -> None:
        """Click source link."""
        self.link_source.click()


class ForeignLink(ClickLinkMixin, POMPage):
    """Foreign navigation links.

    :param Page page: The pytest fixture of ``page``.
    :param str selector: The selector of testing page component.
    """

    def __init__(self, page: Page, selector: str) -> None:
        """Construct the links."""
        super().__init__(page)
        locator = self.page.locator(selector)

        self.link_main = locator.get_by_role(
            'link', name='Иностранный язык',
        )  # fmt: skip
        self.link_exercise = locator.get_by_role(
            'link', name='"Изучение слов"',
        )  # fmt: skip
        self.link_list = locator.get_by_role(
            'link', name='Список слов',
        )  # fmt: skip
        self.link_create = locator.get_by_role(
            'link', name='Добавить слово',
        )  # fmt: skip
        self.link_category = locator.get_by_role(
            'link', name='Категории',
        )  # fmt: skip
        self.link_source = locator.get_by_role(
            'link', name='Источники',
        )  # fmt: skip


class GlossaryLink(ClickLinkMixin, POMPage):
    """Glossary navigation links.

    :param Page page: The pytest fixture of ``page``.
    :param str selector: The selector of testing page component.
    """

    def __init__(self, page: Page, selector: str) -> None:
        """Construct the links."""
        super().__init__(page)
        locator = self.page.locator(selector)

        self.link_main = locator.get_by_role(
            'link', name='Глоссарий',
        )  # fmt: skip
        self.link_exercise = locator.get_by_role(
            'link', name='"Изучение терминов"',
        )  # fmt: skip
        self.link_list = locator.get_by_role(
            'link', name='Список терминов',
        )  # fmt: skip
        self.link_create = locator.get_by_role(
            'link', name='Добавить термин',
        )  # fmt: skip
        self.link_category = locator.get_by_role(
            'link', name='Категории',
        )  # fmt: skip
        self.link_source = locator.get_by_role(
            'link', name='Источники',
        )  # fmt: skip


class MathematicsLink(POMPage):
    """Mathematics navigation links."""

    def __init__(self, page: Page, selector: str) -> None:
        """Construct the links."""
        super().__init__(page)
        locator = self.page.locator(selector)

        self.link_main = locator.get_by_role(
            'link', name='Математика',
        )  # fmt: skip
        self.link_exercise = locator.get_by_role(
            'link', name='"Вычисления"',
        )  # fmt: skip

    def click_link_main(self) -> None:
        """Click main link."""
        self.link_main.click()

    def click_link_exercise(self) -> None:
        """Click exercise link."""
        self.link_exercise.click()
