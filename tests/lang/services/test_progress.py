"""Test Word study progress update service."""

from unittest.mock import Mock

from apps.lang import schemas, types
from apps.lang.services.abc import WordProgressServiceABC


class TestService:
    """Test Word study progress update service."""

    def test_update_progress(
        self,
        mock_progress_repo: Mock,
        mock_django_cache_storage: Mock,
        progress_config: schemas.ProgressConfigSchema,
        progress_case: types.WordProgressType,
        case_data: schemas.WordStudyCaseSchema,
        progress_service_di_mock: WordProgressServiceABC,
    ) -> None:
        """Test Word study progress update service."""
        # Arrange
        mock_django_cache_storage.pop.return_value = case_data

        # Act
        progress_service_di_mock.update_progress(**progress_case)

        # Assert
        mock_django_cache_storage.pop.assert_called_once_with(
            cache_kay=progress_case['case_uuid'],
        )
        mock_progress_repo.update.assert_called_once_with(
            translation_id=case_data.translation_id,
            language=case_data.language,
            progress_case=progress_case['progress_type'],
            progress_value=progress_config.increment,
        )
