"""Language rule views."""

__all__ = [
    # Base
    'BaseRuleDetailView',
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
    # Mentorship
    'RuleStudentView',
    'RuleMentorListView',
    'RuleStudentListView',
]

from .base import (
    BaseRuleDetailView,
)
from .example import (
    RuleExampleView,
    RuleExceptionView,
)
from .mentorship import (
    RuleMentorListView,
    RuleStudentListView,
    RuleStudentView,
)
from .rule import (
    RuleCreateView,
    RuleDeleteView,
    RuleDetailView,
    RuleIndexView,
    RuleListView,
    RuleUpdateView,
)
