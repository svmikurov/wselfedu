"""Language rule views."""

__all__ = [
    # Base
    'BaseRuleDetailView',
    # Rule
    'ClauseCreateView',
    'ClauseUpdateView',
    'RuleView',
    'RuleListView',
    'RuleDetailView',
    'RuleCreateView',
    'RuleUpdateView',
    'RuleDeleteView',
    # Rule example/exception
    'WordExampleAddView',
    'WordExampleListView',
    'WordExampleDeleteView',
    'TaskExampleAddView',
    'TaskExampleListView',
    'TaskExampleDeleteView',
    'ExceptionAddView',
    # Mentorship
    'RuleAssignmentCreate',
]

from .base import (
    BaseRuleDetailView,
)
from .example import (
    ExceptionAddView,
    TaskExampleAddView,
    WordExampleAddView,
    WordExampleDeleteView,
    WordExampleListView,
    TaskExampleDeleteView,
    TaskExampleListView,
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
    RuleListView,
    RuleUpdateView,
    RuleView,
)
