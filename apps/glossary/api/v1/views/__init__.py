"""Glossary app API v1 views."""

__all__ = [
    'TermViewSet',
    'TermStudyViewSet',
]

from .study import TermStudyViewSet
from .term import TermViewSet
