"""Resource type aliases."""

from typing import TypeAlias

from apps.lang.models import EnglishTranslation
from interfaces.protocols.domain.exercise import Candidates

TranslationCandidates: TypeAlias = Candidates[EnglishTranslation]
