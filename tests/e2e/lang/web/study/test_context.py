"""Language discipline translation study context tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from apps.lang import models

if TYPE_CHECKING:
    from django.http.response import HttpResponse
    from django.test import Client

    from apps.lang import types

# TODO: Fix type ignore

STUDY_URL_PATH = reverse('lang:translation_english_study')
STUDY_CASE_URL_PATH = reverse('lang:translation_english_study_case')

# Study settings are stored in the tag data-* attributes
# <div id="..."
#      data-question="{{ task.question_timeout }}"
#       ...>
SETTINGS_TAG_ID = 'settings-block'
DEFAULT_SETTINGS = {
    # Translation parameters
    'category': '',
    'mark': '',
    'source': '',
    'start-period': '',
    'end-period': '',
    # Translation settings
    'translation-order': '',
    'word-count': '',
    # Presentation settings
    'answer': str(models.PresentationSettings.DEFAULT_TIMEOUT),
    'question': str(models.PresentationSettings.DEFAULT_TIMEOUT),
    'url': STUDY_CASE_URL_PATH,
}


@pytest.fixture
def user_settings(
    parameters_db_data: types.SetStudyParameters,
) -> dict[str, Any]:
    """Provide user settings."""
    return {
        # Translation parameters
        'category': str(parameters_db_data['category']['id']),  # type: ignore[index]
        'mark': str(parameters_db_data['mark']['id']),  # type: ignore[index]
        'source': str(parameters_db_data['word_source']['id']),  # type: ignore[index]
        'start-period': str(parameters_db_data['start_period']['id']),  # type: ignore[index]
        'end-period': str(parameters_db_data['end_period']['id']),  # type: ignore[index]
        # Translation settings
        'translation-order': '',
        'word-count': '',
        # Presentation settings
        'answer': str(parameters_db_data['answer_timeout']),
        'question': str(parameters_db_data['question_timeout']),
        'url': STUDY_CASE_URL_PATH,
    }


def extract_attributes(response: HttpResponse, tag_id: str) -> dict[str, Any]:
    """Extract data-* attributes."""
    soup = BeautifulSoup(response.content, 'html.parser')
    tag = soup.find('div', {'id': tag_id})
    if tag is None:
        raise ValueError(f'Page content have no {tag_id!r} ID')
    return {
        key[5:]: value
        for key, value in tag.attrs.items()
        if key.startswith('data-')
    }


@pytest.mark.django_db
class TestSettingsContext:
    """Translation study settings context tests."""

    def test_contains_default_settings(self, auth_client: Client) -> None:
        """Context contains current study settings default data."""
        # Act
        response = auth_client.get(STUDY_URL_PATH)

        # Assert
        data = extract_attributes(response, SETTINGS_TAG_ID)  # type: ignore[arg-type]
        assert data == DEFAULT_SETTINGS

    def test_contains_settings(
        self,
        auth_client: Client,
        user_settings: types.SetStudyParameters,
    ) -> None:
        """Context contains current study settings data."""
        # Act
        response = auth_client.get(STUDY_URL_PATH)

        # Assert
        data = extract_attributes(response, SETTINGS_TAG_ID)  # type: ignore[arg-type]
        assert data == user_settings


@pytest.mark.django_db
class TestInfoContext:
    """Translation study info context tests."""

    def test_info(
        self,
        auth_client: Client,
        english_progress: models.EnglishProgress,
    ) -> None:
        """Test info content."""
        # Act
        response = auth_client.get(STUDY_CASE_URL_PATH)

        # Assert
        assert 'info' in response.context.keys()
        info = response.context.get('info')

        assert info is not None
        assert info.get('progress') == english_progress.progress
