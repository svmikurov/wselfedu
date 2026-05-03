"""Test's dependencies types."""

__all__ = (
    'DomainT',
    'RepositoryT',
    'ServiceT',
    'TaskBuilderT',
    'OptionsDomainT',
    'HandlerT',
    'RequestContextT',
    'RequestDataT',
    'RequestParamsT',
    'TranslationCandidates',
    'TranslationsT',
)

from .handler import (
    DomainT,
    HandlerT,
    OptionsDomainT,
    RepositoryT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
    ServiceT,
    TaskBuilderT,
)
from .resource import (
    TranslationCandidates,
    TranslationsT,
)
