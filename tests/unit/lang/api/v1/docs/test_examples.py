"""API documentation response data example tests."""

from apps.lang.api.v1 import examples, serializers


class TestWordStudy:
    """Word study Presentation data API data examples tests."""

    def test_get_parameters_success_response_data_example(self) -> None:
        """Test that Parameters response data example is correct."""
        serializer = serializers.SetParametersSerializer(
            data=examples.SET_WORD_STUDY_PARAMETERS_DATA
        )
        assert serializer.is_valid()

    def test_get_presentation_case_success(self) -> None:
        """Test that Word case requests data example is correct."""
        serializer = serializers.WordParametersSerializer(
            data=examples.WORD_STUDY_PARAMETERS_DATA
        )
        assert serializer.is_valid()
