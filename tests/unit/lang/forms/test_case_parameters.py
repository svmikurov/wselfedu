"""Case parameters form test.

Form converts and validates request data as form representation of
study settings to get next study case
"""

from typing import Final, Mapping

from django.http import QueryDict

from apps.lang import forms

REQUEST_DATA: Final[Mapping[str, str]] = {
    # Translation parameters
    'category': '1',
    'source': '',
    'start_period': '',
    'end_period': '',
    # Progress phases
    'is_examine': 'true',
    'is_know': 'true',
    'is_repeat': 'false',
    'is_study': 'false',
    # Translation settings
    'translation_order': 'random',
    'word_count': '',
}
REQUEST_LIST_DATA: Final[Mapping[str, list[str]]] = {
    'mark': ['12', '9'],
}

REQUEST_QUERYDICT = QueryDict('', mutable=True)
REQUEST_QUERYDICT.update(REQUEST_DATA)
REQUEST_QUERYDICT.setlist('mark', REQUEST_LIST_DATA['mark'])
REQUEST_QUERYDICT._mutable = False

EXPECTED_CLEANED_DATA: dict[str, int | str | list[int] | None] = {
    # Translation parameters
    'category': 1,
    'source': None,
    'mark': [12, 9],
    'start_period': None,
    'end_period': None,
    # Progress phases
    'is_examine': True,
    'is_know': True,
    'is_repeat': False,
    'is_study': False,
    # Translation settings
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
