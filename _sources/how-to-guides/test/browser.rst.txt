===============
Browser testing
===============

Inherit the page (page component) representation class form :py:class:`~tests_plw.pages.base.POMPage`.

.. code-block:: python

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
           )

       def click_link_profile(self) -> None:
           """Click profile link."""
           self.link_profile.click()

Inherit your test class from :py:class:`~tests_plw.tests.base.POMTest`.

.. code-block:: python

   class TestSidebar(POMTest):
    """Test sidebar."""

    def setUp(self) -> None:
        """Set up page data."""
        self.test_page = SidebarComponent(self.page)
        self.authorize_test_page()

    def test_link_profile(self) -> None:
        """Test the profile link."""
        self.test_page.click_link_profile()
        self.test_page.test_title(ProfilePage.title)

