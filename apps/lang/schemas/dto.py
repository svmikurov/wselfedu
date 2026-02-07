"""Get presentation DTO."""

import uuid
from dataclasses import dataclass

# DEPRECATED: Delete


@dataclass(frozen=True, slots=True)
class TranslationCase:
    """Translation case DTO."""

    question: str
    answer: str
    progress: str


@dataclass(frozen=True, slots=True)
class CaseMeta:
    """Translation case story DTO."""

    pk: int


@dataclass(frozen=True)
class PresentationCase(TranslationCase):
    """Presentation case DTO."""

    case_uuid: uuid.UUID
