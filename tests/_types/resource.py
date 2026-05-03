"""Resource type aliases."""

from typing import Iterable, TypeAlias

from apps.lang.models import EnglishTranslation
from interfaces.protocols.domain.exercise import Candidates

TranslationCandidates: TypeAlias = Candidates
TranslationsT: TypeAlias = Iterable[EnglishTranslation]
