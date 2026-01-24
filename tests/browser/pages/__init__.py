"""Contains pages for browser POM testing."""

__all__ = [
    # Student pages (mentorship)
    'AssignmentsPage',
    # Exercise pages
    'TranslationTestPage',
]

from .lang.student.assignments import AssignmentsPage
from .lang.student.translation_test import TranslationTestPage
