"""Word study Presentation repository test."""

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test.utils import CaptureQueriesContext

from apps.lang import models, repos
from apps.users.models import CustomUser


@pytest.mark.django_db
class TestRepository:
    """Word study Presentation repository test."""

    def test_get_case(
        self,
        user: CustomUser,
        translation: models.EnglishTranslation,
        native_word: models.NativeWord,
        english_word: models.EnglishWord,
        english_progress: models.EnglishProgress,  # Adds progress to DB
        presentation_repo: repos.Presentation,
    ) -> None:
        """Test get Word study Presentation case."""
        # Act
        result = presentation_repo.get_case(
            user=user,
            translation_id=translation.pk,
            language='english',
        )

        # Assert
        assert result['definition'] == english_word.word
        assert result['explanation'] == native_word.word
        assert result['info']['progress'] == english_progress.progress  # type: ignore[index]
        assert len(result) == 3

    def test_get_case_not_found(
        self,
        presentation_repo: repos.Presentation,
        user: CustomUser,
    ) -> None:
        """Test case when translation doesn't exist."""
        # Arrange
        no_exist_translation_id = 999

        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            presentation_repo.get_case(
                user=user,
                translation_id=no_exist_translation_id,
                language='english',
            )

    def test_get_case_different_users(
        self,
        presentation_repo: repos.Presentation,
        other_user: CustomUser,
        translation: models.EnglishTranslation,
    ) -> None:
        """Test that users can only access their own translations."""
        # Act & Assert - other user shouldn't see the translation
        with pytest.raises(ObjectDoesNotExist):
            presentation_repo.get_case(
                user=other_user,
                translation_id=translation.pk,
                language='english',
            )

    def test_get_case_query_count(
        self,
        presentation_repo: repos.Presentation,
        user: CustomUser,
        translation: models.EnglishTranslation,
        django_assert_num_queries: CaptureQueriesContext,
    ) -> None:
        """Test that only one query is executed."""
        # Act & Assert
        with django_assert_num_queries(1):  # type: ignore[operator]
            presentation_repo.get_case(
                user=user, translation_id=translation.pk, language='english'
            )
