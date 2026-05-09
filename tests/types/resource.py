"""Resource type aliases."""

from typing import Iterable, TypeAlias

from apps.lang.models import EnglishTranslation

TranslationsT: TypeAlias = Iterable[EnglishTranslation]
