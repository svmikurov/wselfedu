"""Resource type aliases."""

from typing import Iterable, TypeAlias

from apps.lang.models import EnglishTranslation
from contracts.entity.domain.exercise.fields import Candidates

TranslationCandidates: TypeAlias = Candidates
TranslationsT: TypeAlias = Iterable[EnglishTranslation]
