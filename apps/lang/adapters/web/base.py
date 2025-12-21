"""Translation presentation adapter for WEB context."""

from abc import ABC, abstractmethod

from apps.lang import types


class BaseTranslationAdapterWEB(ABC):
    """ABC for translation presentation adapter for WEB context."""

    @abstractmethod
    def to_context(self, data: types.TranslationCase) -> types.TranslationWEB:
        """Adapt the presentation case of translation for WEB."""
