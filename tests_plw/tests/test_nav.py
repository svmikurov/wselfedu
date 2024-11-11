"""Test the navigation links.

Testing:
* Sidebar link by next page title.

.. todo::

   * add test the Navbar link by next page title.
"""

from tests_plw import pages
from tests_plw.page_components import nav
from tests_plw.tests.base import POMTest


class ForeignLinkMixin:
    """Foreign link target page titles."""

    class_link = nav.ForeignLink

    title_main = pages.ForeignMainPage.title
    title_exercise = pages.ForeignExerciseParamsPage.title
    title_list = pages.ForeignListPage.title
    title_create = pages.ForeignCreatePage.title
    title_category = pages.ForeignCategoryPage.title
    title_source = pages.ForeignSourcePage.title


class GlossaryLinkMixin:
    """Term link target page titles."""

    class_link = nav.GlossaryLink

    title_main = pages.GlossaryPage.title
    title_exercise = pages.GlossaryExercisePage.title
    title_list = pages.TermListPage.title
    title_create = pages.TermCreatePage.title
    title_category = pages.TermCategoryPage.title
    title_source = pages.TermSourcePage.title


class MathematicsLinkMixin:
    """Mathematics link target page titles."""

    class_link = nav.MathematicsLink

    title_main = pages.MathPage.title
    title_exercise = pages.MathExerciseParamsPage.title


class MainTestMixin:
    """Mixin to tests a main links."""

    test_page: nav.MainLink

    title_profile = ''
    title_home = ''
    title_about = ''
    title_mobile = ''

    def test_link_main(self) -> None:
        """Test the main link."""
        self.test_page.click_link_home()
        self.test_page.test_title(self.title_home)

    def test_link_profile(self) -> None:
        """Test the profile link."""
        self.test_page.click_link_profile()
        self.test_page.test_title(self.title_profile)

    def test_link_about(self) -> None:
        """Test the about link."""
        self.test_page.click_link_about()
        self.test_page.test_title(self.title_about)

    def test_link_mobile(self) -> None:
        """Test the mobile link."""
        self.test_page.click_link_mobile()
        self.test_page.test_title(self.title_mobile)


class CommonTestMixin:
    """Mixin to test a common links.

    Common mixin for ForeignLink and GlossaryLink classes.
    """

    test_page: [
        nav.ForeignLink,
        nav.GlossaryLink,
    ]

    __test__ = False

    title_main = ''
    title_exercise = ''
    title_list = ''
    title_create = ''
    title_category = ''
    title_source = ''

    def test_link_main(self) -> None:
        """Test the main link."""
        self.test_page.click_link_main()
        self.test_page.test_title(self.title_main)

    def test_link_exercise(self) -> None:
        """Test the exercise link."""
        self.test_page.click_link_exercise()
        self.test_page.test_title(self.title_exercise)

    def test_link_list(self) -> None:
        """Test the list link."""
        self.test_page.click_link_list()
        self.test_page.test_title(self.title_list)

    def test_link_create(self) -> None:
        """Test the create link."""
        self.test_page.click_link_create()
        self.test_page.test_title(self.title_create)

    def test_link_category(self) -> None:
        """Test the category link."""
        self.test_page.click_link_category()
        self.test_page.test_title(self.title_category)

    def test_link_source(self) -> None:
        """Test the source link."""
        self.test_page.click_link_source()
        self.test_page.test_title(self.title_source)


class MathematicsTestMixin:
    """Mixin to tests a mathematics links."""

    test_page: nav.MathematicsLink

    __test__ = False

    title_main = ''
    title_exercise = ''

    def test_link_main(self) -> None:
        """Test the main link."""
        self.test_page.click_link_main()
        self.test_page.test_title(self.title_main)

    def test_link_exercise(self) -> None:
        """Test the exercise link."""
        self.test_page.click_link_exercise()
        self.test_page.test_title(self.title_exercise)


class LinkTest(POMTest):
    """Run tests of links.

    :var str selector: The selector of testing page component.
    :var int count_link: Number of links in a component. Note that the
        list of items includes a divider at navbar.
    :var class_link: The component representation class.
    """

    selector: str
    count_link: int
    class_link: [
        nav.ForeignLink,
        nav.GlossaryLink,
        nav.MainLink,
        nav.MathematicsLink,
    ]

    __test__ = False

    def setUp(self) -> None:
        """Set up the tests."""
        self.test_page = self.class_link(self.page, self.selector)
        self.authorize_test_page()

    def test_link_count(self) -> None:
        """Test the count of link at navigation chapter."""
        assert (
            self.page.locator(' '.join([self.selector, 'li'])).count()
            == self.count_link
        )


class SidebarForeignTest(ForeignLinkMixin, CommonTestMixin, LinkTest):
    """Test of foreign links at sidebar."""

    __test__ = True
    selector = '[id=sidebar-foreign]'
    count_link = 7


class SidebarGlossaryTest(GlossaryLinkMixin, CommonTestMixin, LinkTest):
    """Test of glossary links at sidebar."""

    __test__ = True
    selector = '[id=sidebar-glossary]'
    count_link = 7


class SidebarMathematicsTest(
    MathematicsLinkMixin,
    MathematicsTestMixin,
    LinkTest,
):
    """Test of mathematics links at sidebar."""

    __test__ = True
    selector = '[id=sidebar-mathematics]'
    count_link = 3
