"""API documentation response data example tests."""

from apps.lang.api.v1 import examples, serializers


class TestWordStudy:
    """Word study Presentation Parameters response data examples."""

    def test_get_parameters_success_response_data_example(self) -> None:
        """Test that Parameters response data example is correct."""
        serializer = serializers.WordStudyPresentationParamsSerializer(
            data=examples.WORD_STUDY_PARAMETERS_DATA
        )
        assert serializer.is_valid()
