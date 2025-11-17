"""Test the Word study Service via presentation."""

from di import MainContainer


class TestCreateService:
    """Test that Word study Service created."""

    def test_create_word_study_presentation_service(
        self,
        container: MainContainer,
    ) -> None:
        """Test that Word study presentation Services was created."""
        service = container.lang.word_presentation_service()
        assert service is not None
