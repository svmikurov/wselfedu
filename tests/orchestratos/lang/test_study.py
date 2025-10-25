"""Test the `WordStudyOrchestrator` that gets word study case."""

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test.utils import CaptureQueriesContext

from apps.lang.models import EnglishTranslation, EnglishWord, NativeWord
from apps.lang.orchestrators.study import WordStudyOrchestrator
from apps.users.models import CustomUser


# TODO: Add test case no candidates to task for specific params
class TestNoCase:
    """Test case no candidates to task for specific params."""

    @pytest.mark.skip
    def test_no_case(self) -> None:
        """Test case no candidates to task for specific params."""


@pytest.mark.django_db
class TestGetCase:
    """Test get_case method."""

    @pytest.fixture
    def user(self) -> CustomUser:
        """User fixture."""
        return CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )

    @pytest.fixture
    def native_word(self, user: CustomUser) -> NativeWord:
        """Native word fixture."""
        return NativeWord.objects.create(user=user, word='дом')

    @pytest.fixture
    def english_word(self, user: CustomUser) -> EnglishWord:
        """English word fixture."""
        return EnglishWord.objects.create(user=user, word='house')

    @pytest.fixture
    def translation(
        self,
        user: CustomUser,
        native_word: NativeWord,
        english_word: EnglishWord,
    ) -> EnglishTranslation:
        """Get translation fixture."""
        return EnglishTranslation.objects.create(
            user=user, native=native_word, english=english_word
        )

    @pytest.fixture
    def service(self) -> WordStudyOrchestrator:
        """Service fixture."""
        return WordStudyOrchestrator()

    def test_get_case_success(
        self,
        service: WordStudyOrchestrator,
        user: CustomUser,
        translation: EnglishTranslation,
        native_word: NativeWord,
        english_word: EnglishWord,
    ) -> None:
        """Test successful case retrieval."""
        # Act
        result = service.get_case(english_word_id=native_word.id, user=user)

        # Assert
        assert result['definition'] == str(english_word)
        assert result['explanation'] == str(native_word)
        assert 'definition' in result
        assert 'explanation' in result
        assert len(result) == 2

    def test_get_case_not_found(
        self,
        service: WordStudyOrchestrator,
        user: CustomUser,
    ) -> None:
        """Test case when translation doesn't exist."""
        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            service.get_case(english_word_id=999, user=user)

    def test_get_case_different_users(
        self,
        service: WordStudyOrchestrator,
        user: CustomUser,
        translation: EnglishTranslation,
    ) -> None:
        """Test that users can only access their own translations."""
        # Create another user
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123',
        )

        # Act & Assert - other user shouldn't see the translation
        with pytest.raises(ObjectDoesNotExist):
            service.get_case(
                english_word_id=translation.native.id, user=other_user
            )

    def test_get_case_query_count(
        self,
        service: WordStudyOrchestrator,
        user: CustomUser,
        translation: EnglishTranslation,
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test that only one query is executed."""
        with django_assert_num_queries(1):  # type: ignore[operator]
            result = service.get_case(
                english_word_id=translation.native.id, user=user
            )

        assert 'definition' in result
        assert 'explanation' in result
        assert result['definition'] == str(translation.english)
        assert result['explanation'] == str(translation.native)
