"""Test Word study progress repository."""

import pytest

from apps.lang import models, repositories
from apps.users.models import Person


@pytest.mark.django_db
class TestRepository:
    """Test Word study progress repository."""

    @pytest.mark.parametrize(
        'progress_delta, expected_progress',
        [
            (1, 1),
            (-1, 0),
            (
                models.EnglishProgress.MAX_PROGRESS + 1,
                models.EnglishProgress.MAX_PROGRESS,
            ),
        ],
    )
    def test_create_progress(
        self,
        progress_delta: int,
        expected_progress: int,
        user: Person,
        word_translation: models.EnglishTranslation,
        progress_repo: repositories.Progress,
    ) -> None:
        """Test create the Word study progress."""
        # Act
        progress_repo.update(
            user=user,
            translation_id=word_translation.pk,
            language='english',
            progress_delta=progress_delta,
        )

        # Assert
        progress = models.EnglishProgress.objects.get(
            translation_id=word_translation.pk,
        )
        assert progress.progress == expected_progress

    @pytest.mark.parametrize(
        'initial_progress, progress_delta, expected_progress',
        [
            (0, 1, 1),
            (0, -1, 0),
            (1, -1, 0),
            (
                models.EnglishProgress.MAX_PROGRESS - 1,
                2,
                models.EnglishProgress.MAX_PROGRESS,
            ),
        ],
    )
    def test_update_progress(
        self,
        initial_progress: int,
        progress_delta: int,
        expected_progress: int,
        user: Person,
        word_translation: models.EnglishTranslation,
        progress_repo: repositories.Progress,
    ) -> None:
        """Test update the Word study progress."""
        # Average
        models.EnglishProgress.objects.create(
            user=user,
            translation_id=word_translation.pk,
            progress=initial_progress,
        )

        # Act
        progress_repo.update(
            user=user,
            translation_id=word_translation.pk,
            language='english',
            progress_delta=progress_delta,
        )

        # Assert
        progress = models.EnglishProgress.objects.get(
            translation_id=word_translation.pk,
        )
        assert progress.progress == expected_progress
