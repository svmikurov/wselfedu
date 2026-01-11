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
    'ClauseCreateView',
    'ClauseUpdateView',
    'ClauseExampleView',
    'RuleExceptionView',
    'ClauseTaskExampleView',
    # Mentorship
    'RuleAssignmentCreate',
]

from .base import (
    BaseRuleDetailView,
)
from .example import (
    ClauseExampleView,
    ClauseTaskExampleView,
    RuleExceptionView,
)
from .mentorship import (
    RuleAssignmentCreate,
)
from .rule import (
    ClauseCreateView,
    ClauseUpdateView,
    RuleCreateView,
    RuleDeleteView,
    RuleDetailView,
    RuleIndexView,
    RuleListView,
    RuleUpdateView,
)
