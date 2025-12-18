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


STUDY_URL_PATH = reverse('lang:translation_english_study')
STUDY_CASE_URL_PATH = reverse('lang:translation_english_study_case')

# Study settings are stored in the tag data-* attributes
# <div id="..."
#      data-question="{{ task.question_timeout }}"
#       ...>
SETTINGS_TAG_ID = 'settings-block'
EXPECTED_STUDY_SETTINGS = {
    'answer': '3',
    'question': '3',
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
        assert data == EXPECTED_STUDY_SETTINGS


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
