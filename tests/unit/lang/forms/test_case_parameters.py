"""Case parameters form test."""

from typing import Final, Mapping

from django.http import QueryDict

from apps.lang import forms

REQUEST_DATA: Final[Mapping[str, str]] = {
    'category': '1',
    'source': '',
    'start_period': '',
    'end_period': '',
    'translation_order': 'random',
    'word_count': '',
}
REQUEST_LIST_DATA: Final[Mapping[str, list[str]]] = {
    'marks': ['12', '9'],
}

REQUEST_QUERYDICT = QueryDict('', mutable=True)
REQUEST_QUERYDICT.update(REQUEST_DATA)
REQUEST_QUERYDICT.setlist('marks', REQUEST_LIST_DATA['marks'])
REQUEST_QUERYDICT._mutable = False

EXPECTED_CLEANED_DATA: dict[str, int | str | list[int] | None] = {
    'category': 1,
    'source': None,
    'marks': [12, 9],
    'start_period': None,
    'end_period': None,
    'translation_order': 'random',
    'word_count': None,
}


class TestCaseParametersForm:
    """Case parameters form test."""

    def test_form_converts_request_to_python_types(self) -> None:
        """Form converts string request data to proper Python types."""
        # Act
        form = forms.CaseRequestForm(REQUEST_QUERYDICT)

        # Assert
        assert form.is_valid(), f'Form errors: {form.errors}'

        assert form.cleaned_data == EXPECTED_CLEANED_DATA
