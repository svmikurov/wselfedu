"""Test the `WordStudyRepository` that gets word study case."""

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test.utils import CaptureQueriesContext

from apps.lang import models
from apps.lang.repos.presentation import Presentation
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
    def service(self) -> Presentation:
        """Service fixture."""
        return Presentation()

    def test_get_case_success(
        self,
        service: Presentation,
        user: CustomUser,
        translation: models.EnglishTranslation,  # Adds translation to DB
        native_word: models.NativeWord,
        english_word: models.EnglishWord,
    ) -> None:
        """Test successful case retrieval."""
        # Act
        result = service.get_case(
            user=user, translation_id=translation.pk, language='english'
        )

        # Assert
        assert result['definition'] == str(english_word)
        assert result['explanation'] == str(native_word)
        assert 'definition' in result
        assert 'explanation' in result
        assert len(result) == 2

    def test_get_case_not_found(
        self,
        service: Presentation,
        user: CustomUser,
    ) -> None:
        """Test case when translation doesn't exist."""
        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            service.get_case(user=user, translation_id=999, language='english')

    def test_get_case_different_users(
        self,
        service: Presentation,
        user: CustomUser,  # Adds user to DB
        translation: models.EnglishTranslation,
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
                user=other_user,
                translation_id=translation.pk,
                language='english',
            )

    def test_get_case_query_count(
        self,
        service: Presentation,
        user: CustomUser,
        translation: models.EnglishTranslation,
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test that only one query is executed."""
        with django_assert_num_queries(1):  # type: ignore[operator]
            result = service.get_case(
                user=user, translation_id=translation.pk, language='english'
            )

        assert 'definition' in result
        assert 'explanation' in result
        assert result['definition'] == str(translation.english)
        assert result['explanation'] == str(translation.native)
