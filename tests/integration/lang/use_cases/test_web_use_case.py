"""Web get presentation UseCase tests."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import pytest
from django.http import QueryDict

from apps.lang import use_cases
from apps.lang.schemas import dto
from tests.fixtures.lang.no_db import presentation as fixtures
from tests.fixtures.lang.no_db.translations import TRANSLATIONS

if TYPE_CHECKING:
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
