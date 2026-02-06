"""Test fixture."""

import uuid
from typing import Final

from apps.core.adapter.response.exercise.presentation import (
    PresentationApi,
    PresentationWeb,
    Progress,
    UpdateProgress,
)
from apps.core.domain.exercise.presentation_dto import PresentationData

from .types import PresentationCaseDict

CASE_UUID: Final[uuid.UUID] = uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4')

# ---------------------------------------------------------------------
# Presentation exercise fixtures
# ---------------------------------------------------------------------

# Presentation exercise raw data
# ------------------------------
PRESENTATION_CASE: Final[PresentationCaseDict] = {
    'question_text': 'house',
    'answer_text': 'дом',
    'progress': 7,
}
PRESENTATION_CASE_STORED: Final = {'case_uuid': CASE_UUID, **PRESENTATION_CASE}

# Presentation exercise DTO
# -------------------------
PRESENTATION_DOMAIN_DTO = PresentationData(**PRESENTATION_CASE_STORED)  # type: ignore[arg-type]
PRESENTATION_API_DTO = PresentationApi(**PRESENTATION_CASE_STORED)  # type: ignore[arg-type]
PRESENTATION_WEB_DTO = PresentationWeb(
    case_uuid=CASE_UUID,
    question_text=PRESENTATION_CASE['question_text'],
    answer_text=PRESENTATION_CASE['answer_text'],
    progress=Progress(
        current_value=PRESENTATION_CASE['progress'],
        update_endpoint='/api/v1/lang/study/progress/',
        increment_payload=UpdateProgress(case_uuid=CASE_UUID, is_known=True),
        decrement_payload=UpdateProgress(case_uuid=CASE_UUID, is_known=False),
    ),
)
