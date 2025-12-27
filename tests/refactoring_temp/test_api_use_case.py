"""Api get presentation UseCase tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.lang.use_cases import ApiPresentationUseCase

if TYPE_CHECKING:
    from unittest.mock import Mock


class TestWebUseCase:
    """Api get presentation UseCase tests."""

    def test_initialize(
        self,
        mock_validator: Mock,
        mock_service: Mock,
        mock_response_adapter: Mock,
    ) -> None:
        """Api get presentation UseCase initialization."""
        # Act
        use_case = ApiPresentationUseCase(
            validator=mock_validator,
            service=mock_service,
            response_adapter=mock_response_adapter,
        )

        # Assert
        assert use_case is not None
