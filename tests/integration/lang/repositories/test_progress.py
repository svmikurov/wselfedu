"""Test Word study progress repository."""

import pytest

from apps.lang import models, repositories
from apps.study import models as study_models
from apps.users.models import Person


@pytest.mark.django_db
class TestRepository:
    """Test Word study progress repository."""

    @pytest.mark.parametrize(
        'initial_progress, progress_delta, expected_progress',
        [
            (0, 1, 1),
            (0, -1, 0),
            (1, -1, 0),
            (
                study_models.Progress.KNOW_DEFAULT - 1,
                2,
                study_models.Progress.KNOW_DEFAULT,
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
        word_translation.progress = initial_progress
        word_translation.save()

        # Act
        progress_repo.update(
            user=user,
            translation_id=word_translation.pk,
            progress_delta=progress_delta,
        )

        # Assert
        progress = models.EnglishTranslation.objects.get(
            pk=word_translation.pk,
        )
        assert progress.progress == expected_progress
