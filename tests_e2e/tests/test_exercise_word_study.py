import pytest
from playwright.sync_api import expect

from tests_e2e.pages.exercise_word_choice import WordChoiceExercisePage
from tests_e2e.pages.exercise_word_study import WordStudyExercisePage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import PageFixtureTestCase


class TestWordStudyExercisePage(PageFixtureTestCase):
    """The word study exercise page test class."""

    fixtures = ['tests_e2e/fixtures/fixture-db-exercise-word-study']

    def setUp(self) -> None:
        """Choice words according to the user's exercise conditions.

        Authorizes the page before.
        """
        authorize_the_page(self.page, self.live_server_url)
        word_choice_page = WordChoiceExercisePage(self.page)
        word_choice_page.navigate(host=self.live_server_url)
        word_choice_page.choice_word(question_language='EN')

    def test_word_visible(self) -> None:
        """Test the display of the words being studied on page."""
        question_word = self.page.get_by_text('test word')
        answer_word = self.page.get_by_text('тестовое слово')

        expect(question_word).to_be_visible()
        expect(answer_word).to_be_hidden()
        # answer word becomes visible on the timer
        expect(answer_word).not_to_be_hidden()

    def test_favorite_word_button(self) -> None:
        """Test change word favorite status button."""
        word_study_page = WordStudyExercisePage(self.page)
        # The word is not in favorites, by default
        word_study_page.pause_button.click()
        expect(word_study_page.add_to_favorite_button).to_be_visible()
        # Click the "Add to Favorites" button to make the word a
        # favorite
        word_study_page.add_to_favorite_button.click()
        expect(word_study_page.remove_from_favorite_button).to_be_visible()
        # Click the "Remove from favorites" button to remove the word
        # from your favorites
        word_study_page.remove_from_favorite_button.click()
        expect(word_study_page.add_to_favorite_button).to_be_visible()

    def test_knowledge_buttons(self) -> None:
        """Test user`s word knowledge assessment change buttons."""
        word_study_page = WordStudyExercisePage(self.page)
        default_knowledge_assessment = '0'
        assessment_step = '1'

        # word has`t assessment by default
        expect(word_study_page.word_knowledge_indicator).to_contain_text(
            default_knowledge_assessment,
        )
        # clicking on the "Know" button increases the assessment
        # by one step
        word_study_page.know_button.click()
        expect(word_study_page.word_knowledge_indicator).to_contain_text(
            assessment_step,
        )
        # clicking on the "Know" button decreases the assessment
        # by one step
        word_study_page.not_know_button.click()
        expect(word_study_page.word_knowledge_indicator).to_contain_text(
            default_knowledge_assessment,
        )

    @pytest.mark.skip('Add test code')
    def test_pause_button(self) -> None:
        """Test pause button."""

    @pytest.mark.skip('Add test code')
    def test_next_button(self) -> None:
        """Test next button."""
