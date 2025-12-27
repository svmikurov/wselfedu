"""Web get presentation UseCase tests."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import pytest
from django.http import QueryDict

from apps.lang import use_cases
from apps.lang.schemas import dto
from tests.fixtures.lang.no_db.translations import TRANSLATIONS

from . import fixtures

if TYPE_CHECKING:
    from unittest.mock import Mock

    from apps.lang import models
    from apps.users.models import Person

    # Dependency types
    type WebUseCase = use_cases.WebPresentationUseCase

    # Data types
    type Translations = list[models.EnglishTranslation]


class TestWebUseCase:
    """Web get presentation UseCase tests."""

    @pytest.mark.django_db
    def test_request_case_success(
        self,
        web_use_case: WebUseCase,
        user: Person,
        translations: Translations,  # Populate DB
    ) -> None:
        """Get presentation case."""
        # Arrange
        request = fixtures.EMPTY_WEB_REQUEST.copy()
        # - Only last translation for random choice
        request['word_count'] = '1'
        first_translation_index = 0

        request_querydict = QueryDict('', mutable=True)
        request_querydict.update(request)  # type: ignore[arg-type]
        request_querydict._mutable = False

        # - Last translation case
        expected = dto.PresentationCase(
            question=TRANSLATIONS[first_translation_index][1],
            answer=TRANSLATIONS[first_translation_index][0],
            progress='0',
            case_uuid=uuid.uuid4(),
        )

        # Act
        result = web_use_case.execute(user, request_querydict.dict())

        # Assert
        assert result['question'] == expected.question
        assert result['answer'] == expected.answer
        assert result['progress']['current'] == expected.progress

    def test_initialize(
        self,
        mock_validator: Mock,
        mock_service: Mock,
        mock_response_adapter: Mock,
    ) -> None:
        """Web get presentation UseCase initialization."""
        # Act
        use_case = use_cases.WebPresentationUseCase(
            validator=mock_validator,
            service=mock_service,
            response_adapter=mock_response_adapter,
        )

        # Assert
        assert use_case is not None
