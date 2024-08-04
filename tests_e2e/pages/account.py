from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class AccountPage(POMPage):
    def __init__(self, page: Page, host: str | None = None) -> None:
        super().__init__(page)
        self.path = ''
        self.title = 'Личный кабинет'
        self.mult_table_btn = self.page.get_by_role(
            'button',
            name='Таблица умножения',
        )

    def start_study_mult_table(self):
        self.mult_table_btn.click()
