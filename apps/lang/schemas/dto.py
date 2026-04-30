"""Get presentation DTO."""

import uuid

from contracts.schemas.base import BaseDTO

# DEPRECATED: Delete


class TranslationCase(BaseDTO):
    """Translation case DTO."""

    question: str
    answer: str
    progress: str


class CaseMeta(BaseDTO):
    """Translation case story DTO."""

    pk: int


class PresentationCase(TranslationCase):
    """Presentation case DTO."""

    case_uuid: uuid.UUID
