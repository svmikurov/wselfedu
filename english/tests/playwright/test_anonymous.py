"""
Test actions and views for anonymous.
"""
from playwright.sync_api import Page, expect


class TestAnonymous:
    """Test actions and views for anonymous."""

    # @pytest.mark.skip
    def test_home_page_status(self, page: Page, live_server):
        """Test home page status for anonymous."""
        response = page.request.get(live_server.url)
        expect(response).to_be_ok()

    # @pytest.mark.skip
    def test_home_page_title(self, test_page: Page):
        """Test home page content for anonymous."""
        expect(test_page).to_have_title('WSE: Домашняя страница')

    # @pytest.mark.skip
    def test_home_page_navbar(self, test_page: Page):
        """Test home page content for anonymous."""
        locators = (
            ('link', 'WSE'),
            ('link', 'Английский язык'),
            ('link', 'Войти'),
            ('link', 'Регистрация'),
        )
        for loc in locators:
            expect(test_page.get_by_role(loc[0], name=loc[1])).to_be_visible()

    # @pytest.mark.skip
    def test_home_page_content(self, test_page: Page):
        """Test home page content for anonymous."""
        home_url = test_page.url

        test_page.get_by_role('button', name='Упражнение \"Изучаем слова\"').click()
        expect(test_page).to_have_title('Изучаем слова')

        test_page.goto(home_url)
        test_page.get_by_role('button', name='Добавить слово в словарь').click()
        expect(test_page).to_have_title('Добавить слово')
