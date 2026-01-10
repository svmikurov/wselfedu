"""Language application web adapter base classes."""

from abc import ABC, abstractmethod

from .. import models
from . import dto


class WebRuleAdapterABC(ABC):
    """ABC for language rule web adapter."""

    @abstractmethod
    def to_response(self, query: models.Rule) -> dto.RuleSchema:
        """Convert rule queryset to web representation context."""
