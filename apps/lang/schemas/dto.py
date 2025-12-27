"""Get presentation DTO."""

import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TranslationCase:
    """Translation case DTO."""

    question: str
    answer: str
    progress: str


@dataclass(frozen=True, slots=True)
class CaseMeta:
    """Translation case story DTO."""

    id: int


@dataclass(frozen=True)
class PresentationCase(TranslationCase):
    """Presentation case DTO."""

    case_uuid: uuid.UUID
