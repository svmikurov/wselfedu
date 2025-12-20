"""Language discipline translation study context tests."""

from __future__ import annotations

import json
import uuid
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

import di
from apps.lang import models
from apps.lang.services import WordPresentationServiceABC

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
    # Meta
    'url': STUDY_CASE_URL_PATH,
}


@pytest.fixture
def user_settings(
    parameters_db_data: types.CaseSettings,
) -> dict[str, Any]:
    """Provide translation study settings of user.

    Populates the database with the translation study settings
    set by the user.

    Return:
    ------
        Translation study settings data.

    """
    return {
        # Translation meta
        'category': str(parameters_db_data['category']['id']),  # type: ignore[index]
        'mark': str(parameters_db_data['mark']['id']),  # type: ignore[index]
        'source': str(parameters_db_data['word_source']['id']),  # type: ignore[index]
        'start-period': str(parameters_db_data['start_period']['id']),  # type: ignore[index]
        'end-period': str(parameters_db_data['end_period']['id']),  # type: ignore[index]
        # Translation settings
        'translation-order': str(
            parameters_db_data['translation_order']['code']  # type: ignore[index]
        ),
        'word-count': str(parameters_db_data['word_count']),
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
    """Translation study settings tests."""

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
        user_settings: types.CaseSettings,
    ) -> None:
        """Context contains current study settings data."""
        # Act
        response = auth_client.get(STUDY_URL_PATH)

        # Assert
        data = extract_attributes(response, SETTINGS_TAG_ID)  # type: ignore[arg-type]
        assert data == user_settings


@pytest.mark.django_db
class TestCaseContext:
    """Translation study settings case tests."""

    def test_have_correct_context(
        self,
        auth_client: Client,
        case_uuid: uuid.UUID,
        parameters_db_data: dict[str, Any],
    ) -> None:
        """Study settings response have correct context."""
        # Arrange
        # - set translation study data to return
        #   by translation study service
        case: types.PresentationCaseT = {
            'case_uuid': case_uuid,
            'definition': 'test',
            'explanation': 'test',
            'info': {
                'progress': 1,
            },
        }
        # - build study service mock
        study_service_mock = Mock(spec=WordPresentationServiceABC)
        study_service_mock.get_presentation_case.return_value = case

        # Act
        # - mock study service
        with di.container.lang.word_presentation_service.override(
            study_service_mock
        ):
            context = auth_client.get(
                STUDY_CASE_URL_PATH,
                data=parameters_db_data,
            ).context

        # Assert
        # - translation study case is correct
        assert context['case'] == case

        # - translation meta data is correct
        assert context['info'] == case['info']

        # - payload to update translation study progress is correct
        assert json.loads(context['task']['known']) == {
            'case_uuid': str(case_uuid),
            'is_known': True,
        }
        assert json.loads(context['task']['unknown']) == {
            'case_uuid': str(case_uuid),
            'is_known': False,
        }
