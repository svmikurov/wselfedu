"""Language rule views."""

__all__ = [
    # Rule
    'RuleIndexView',
    'RuleListView',
    'RuleDetailView',
    'RuleCreateView',
    'RuleUpdateView',
    'RuleDeleteView',
    # Rule example/exception
    'RuleExampleView',
    'RuleExceptionView',
    # Student
    'RuleStudentView',
]

from .rule import (
    RuleCreateView,
    RuleDeleteView,
    RuleDetailView,
    RuleIndexView,
    RuleListView,
    RuleUpdateView,
)
from .example import (
    RuleExampleView,
    RuleExceptionView,
)
from .mentorship import (
    RuleStudentView,
    RuleStudentListView,
    RuleMentorListView,
)
