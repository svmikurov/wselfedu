"""Test Word study progress update service."""

from unittest.mock import Mock

from apps.lang import schemas, types
from apps.lang.services.abc import WordProgressServiceABC


class TestService:
    """Test Word study progress update service."""

    def test_update_progress(
        self,
        mock_user: Mock,
        mock_progress_repo: Mock,
        mock_django_cache_storage: Mock,
        progress_config: schemas.ProgressConfigSchema,
        progress_case: types.WordProgressT,
        stored_case: schemas.WordStudyStoredCase,
        progress_service_di_mock: WordProgressServiceABC,
    ) -> None:
        """Test Word study progress update service."""
        # Arrange
        mock_django_cache_storage.pop.return_value = stored_case

        # Act
        progress_service_di_mock.update_progress(mock_user, progress_case)

        # Assert
        mock_django_cache_storage.pop.assert_called_once_with(
            cache_kay=progress_case['case_uuid'],
        )
        mock_progress_repo.update.assert_called_once_with(
            user=mock_user,
            translation_id=stored_case.translation_id,
            language=stored_case.language,
            progress_delta=progress_config.increment,
        )
