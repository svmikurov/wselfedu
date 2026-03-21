"""Test Word study progress repository."""

import pytest

from apps.lang import models, repositories
from apps.lang.repositories import AssignedTranslationProgressRepository
from apps.study import models as study_models
from apps.users.models import Person


@pytest.mark.django_db
class TestAssignedTranslationProgressRepository:
    """Test Assigned English translation study progress repository."""

    _model = models.EnglishTranslationProgress
    ASSIGNED_TRANSLATION_MAX_PROGRESS = 16

    @pytest.mark.parametrize(
        'initial_progress, progress_delta, expected_progress',
        [
            (0, 1, 1),
            (0, -1, 0),
            (1, -1, 0),
            (
                ASSIGNED_TRANSLATION_MAX_PROGRESS - 1,
                2,
                ASSIGNED_TRANSLATION_MAX_PROGRESS,
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
        assigned_progress_repository: AssignedTranslationProgressRepository,
    ) -> None:
        """Test update assigned English translation study progress."""
        # Average
        progress = self._model.objects.create(
            user=user,
            translation=word_translation,
            value=initial_progress,
        )

        # Act
        assigned_progress_repository.update(
            user_pk=user.pk,
            translation_pk=word_translation.pk,
            delta=progress_delta,
            max_progress=self.ASSIGNED_TRANSLATION_MAX_PROGRESS,
        )

        # Assert
        progress = self._model.objects.get(
            user=user, translation=word_translation
        )
        assert progress.value == expected_progress


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
                study_models.ProgressBar.KNOW_DEFAULT - 1,
                2,
                study_models.ProgressBar.KNOW_DEFAULT,
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
        repository: repositories.ProgressRepository,
    ) -> None:
        """Test update the Word study progress."""
        # Average
        word_translation.progress = initial_progress
        word_translation.save()

        # Act
        repository.update(
            user=user,
            pk=word_translation.pk,
            delta=progress_delta,
        )

        # Assert
        progress = models.EnglishTranslation.objects.get(
            pk=word_translation.pk,
        )
        assert progress.progress == expected_progress
