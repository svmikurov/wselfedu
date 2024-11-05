"""Test sidebar."""

from tests_plw.pages import (
    ForeignCategoryPage,
    ForeignCreatePage,
    ForeignExerciseParamsPage,
    ForeignListPage,
    ForeignPage,
    ForeignSourcePage,
    GlossaryExercisePage,
    GlossaryPage,
    MathExercisePage,
    MathPage,
    ProfilePage,
    TermCategoryPage,
    TermCreatePage,
    TermListPage,
    TermSourcePage,
)
from tests_plw.page_components.sidebar import SidebarComponent
from tests_plw.tests.base import POMTest


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

    def test_link_foreign(self) -> None:
        """Test the foreign links."""
        self.test_page.click_link_foreign()
        self.test_page.test_title(ForeignPage.title)

    def test_link_foreign_exercise(self) -> None:
        """Test the foreign exercise links."""
        self.test_page.click_link_foreign_exercise()
        self.test_page.test_title(ForeignExerciseParamsPage.title)

    def test_link_foreign_list(self) -> None:
        """Test the foreign list links."""
        self.test_page.click_link_foreign_list()
        self.test_page.test_title(ForeignListPage.title)

    def test_link_foreign_create(self) -> None:
        """Test the foreign term create link."""
        self.test_page.click_link_foreign_create()
        self.test_page.test_title(ForeignCreatePage.title)

    def test_link_foreign_source(self) -> None:
        """Test the foreign term source link."""
        self.test_page.click_link_foreign_source()
        self.test_page.test_title(ForeignSourcePage.title)

    def test_link_foreign_category(self) -> None:
        """Test the foreign term category link."""
        self.test_page.click_link_foreign_category()
        self.test_page.test_title(ForeignCategoryPage.title)

    def test_link_glossary(self) -> None:
        """Test the glossary link."""
        self.test_page.click_link_glossary()
        self.test_page.test_title(GlossaryPage.title)

    def test_link_glossary_exercise(self) -> None:
        """Test the glossary exercise link."""
        self.test_page.click_link_glossary_exercise()
        self.test_page.test_title(GlossaryExercisePage.title)

    def test_link_glossary_list(self) -> None:
        """Test the glossary term list link."""
        self.test_page.click_link_glossary_list()
        self.test_page.test_title(TermListPage.title)

    def test_link_glossary_create(self) -> None:
        """Test the glossary term create link."""
        self.test_page.click_link_glossary_create()
        self.test_page.test_title(TermCreatePage.title)

    def test_link_glossary_category(self) -> None:
        """Test the glossary term category link."""
        self.test_page.click_link_glossary_category()
        self.test_page.test_title(TermCategoryPage.title)

    def test_link_glossary_source(self) -> None:
        """Test the glossary term source link."""
        self.test_page.click_link_glossary_source()
        self.test_page.test_title(TermSourcePage.title)

    def test_link_mathematics(self) -> None:
        """Test the mathematics link."""
        self.test_page.click_link_math()
        self.test_page.test_title(MathPage.title)

    def test_link_mathematics_exercise(self) -> None:
        """Test the mathematics exercise link."""
        self.test_page.click_link_math_exercise()
        self.test_page.test_title(MathExercisePage.title)
