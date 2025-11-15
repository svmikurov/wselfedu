"""Word study Presentation repository test."""

from apps.lang import repos


class TestRepository:
    """Word study Presentation repository test."""

    def test_get_case(
        self,
        presentation_repo: repos.Presentation,
    ) -> None:
        """Test get Word study Presentation case."""
        # Act
