"""Language discipline translation study context tests."""

from __future__ import annotations

import uuid
from http import HTTPStatus
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
    'mark': '[]',
    'source': '',
    'start-period': '',
    'end-period': '',
    # Translation settings
    'translation-order': 'to_native',
    'word-count': '',
    # Presentation settings
    'answer': str(models.PresentationSettings.DEFAULT_TIMEOUT),
    'question': str(models.PresentationSettings.DEFAULT_TIMEOUT),
    # Meta
    # TODO: Rename to 'case_url'?
    'url': STUDY_CASE_URL_PATH,
}


@pytest.fixture
def user_settings(
    parameters_db_data: types.CaseSettingsAPI,
) -> dict[str, Any]:
    """Provide translation study settings of user.

    Populates the database with the translation study settings
    set by the user.

    Return:
    ------
        Translation study settings data.

    """
    mark = [str(item['id']) for item in parameters_db_data['mark']]
    return {
        # Translation meta
        'category': str(parameters_db_data['category']['id']),  # type: ignore[index]
        'mark': f'{mark}',
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
        user_settings: types.CaseSettingsAPI,
    ) -> None:
        """Context contains current study settings data."""
        # Act
        response = auth_client.get(STUDY_URL_PATH)

        # Assert
        data = extract_attributes(response, SETTINGS_TAG_ID)  # type: ignore[arg-type]
        assert data == user_settings


@pytest.mark.django_db
class TestCaseContext:
    """Translation study case context tests."""

    @pytest.fixture
    def study_settings(
        self,
        parameters_db_data: dict[str, Any],
    ) -> types.CaseSettingsWEB:
        """Provide case study settings."""
        return {
            # Translation parameters
            'category': '',
            'word_source': '',
            'mark': '[]',
            'start_period': '',
            'end_period': '',
            # Progress phases
            'is_study': '',
            'is_repeat': '',
            'is_examine': '',
            'is_know': '',
            # Translation settings
            'translation_order': 'random',
            'word_count': '',
        }

    @pytest.fixture
    def case(self, case_uuid: uuid.UUID) -> types.TranslationCase:
        """Provide case."""
        return {
            'case_uuid': case_uuid,
            'definition': 'test',
            'explanation': 'test',
            'info': {
                'progress': 1,
            },
        }

    def test_status_code(
        self,
        auth_client: Client,
        parameters_db_data: dict[str, Any],
        study_settings: types.CaseSettingsWEB,  # Request case settings
        case: types.TranslationCase,
    ) -> None:
        """Study response status code success test."""
        study_service_mock = Mock(spec=WordPresentationServiceABC)
        study_service_mock.get_case.return_value = case

        # Act
        # - mock study service
        with di.container.lang.word_presentation_service.override(
            study_service_mock
        ):
            response = auth_client.post(
                STUDY_CASE_URL_PATH,
                data=study_settings,
            )

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_have_correct_context(
        self,
        auth_client: Client,
        parameters_db_data: dict[str, Any],  # Populate DB
        study_settings: types.CaseSettingsWEB,  # Request case settings
        case: types.TranslationCase,  # Expected case
        case_uuid: uuid.UUID,
    ) -> None:
        """Study settings response have correct context."""
        study_service_mock = Mock(spec=WordPresentationServiceABC)
        study_service_mock.get_case.return_value = case

        # Act
        # - mock study service
        with di.container.lang.word_presentation_service.override(
            study_service_mock
        ):
            response = auth_client.post(
                STUDY_CASE_URL_PATH,
                data=study_settings,
            )

        # Assert
        context = response.context
        assert context is not None

        # - translation study case is correct
        assert 'case' in context
        assert context['case']['case_uuid'] == str(case['case_uuid'])
        assert context['case']['definition'] == case['definition']
        assert context['case']['explanation'] == case['explanation']

        # - translation meta data is correct
        assert context['case']['progress']['current'] == str(
            case['info']['progress']
        )

    def test_template_contains(
        self,
        auth_client: Client,
        parameters_db_data: dict[str, Any],  # Populate DB
        study_settings: types.CaseSettingsWEB,  # Request case settings
        case: types.TranslationCase,  # Expected case
    ) -> None:
        """Test that template contains case data."""
        study_service_mock = Mock(spec=WordPresentationServiceABC)
        study_service_mock.get_case.return_value = case

        # Act
        # - mock study service
        with di.container.lang.word_presentation_service.override(
            study_service_mock
        ):
            response = auth_client.post(
                STUDY_CASE_URL_PATH,
                data=study_settings,
            )

        # Assert
        soup = BeautifulSoup(response.content, 'html.parser')

        # - template have correct question
        question_tag = soup.find('div', {'id': 'question'})
        assert question_tag.text == case['definition']  # type: ignore[union-attr]

        # - template have correct answer
        answer_tag = soup.find('div', {'id': 'answer'})
        assert answer_tag.text == case['explanation']  # type: ignore[union-attr]
