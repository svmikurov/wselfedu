"""Test Word study progress update service."""

from unittest.mock import Mock

from apps.core.domain.exercise import ProgressConfigSchema
from apps.lang import types
from apps.lang.schemas import dto
from apps.lang.use_cases.exercise.abc import WordProgressServiceABC


class TestService:
    """Test Word study progress update service."""

    def test_update_progress(
        self,
        mock_user: Mock,
        mock_progress_repo: Mock,
        mock_task_storage: Mock,
        progress_config: ProgressConfigSchema,
        progress_case: types.ProgressCase,
        stored_case: dto.CaseMeta,
        progress_service_di_mock: WordProgressServiceABC,
    ) -> None:
        """Test Word study progress update service."""
        # Arrange
        mock_task_storage.retrieve_task.return_value = stored_case

        # Act
        progress_service_di_mock.update_progress(mock_user, progress_case)

        # Assert
        mock_task_storage.retrieve_task.assert_called_once_with(
            uid=progress_case['case_uuid'],
        )
        mock_progress_repo.update.assert_called_once_with(
            user=mock_user,
            pk=stored_case.pk,
            delta=progress_config.increment,
        )
