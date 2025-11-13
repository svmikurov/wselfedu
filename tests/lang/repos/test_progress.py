"""Test Word study progress repository."""

import pytest

from apps.lang import models, repos, schemas, types
from apps.users.models import CustomUser


@pytest.fixture
def progress_repo() -> repos.UpdateWordProgressRepo:
    """Provide Word study update progress repo."""
    return repos.UpdateWordProgressRepo()


@pytest.mark.django_db
class TestRepository:
    """Test Word study progress repository."""

    def test_update(
        self,
        user: CustomUser,
        translation: models.EnglishTranslation,
        progress_config: schemas.ProgressConfigSchema,
        progress_case: types.WordProgressType,
        progress_repo: repos.UpdateWordProgressRepo,
    ) -> None:
        """Test update the Word study progress."""
        progress_repo.update(
            translation_id=translation.pk,
            language='english',
            progress_case=progress_case['progress_type'],
            progress_value=progress_config.increment,
        )

        progress = models.EnglishProgress.objects.get(
            translation_id=translation.pk,
        )
        assert progress.progress == 1
