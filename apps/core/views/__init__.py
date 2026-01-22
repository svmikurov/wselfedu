"""Core views and mixins."""

__all__ = [
    # Authentication
    'OwnerMixin',
    'OwnershipRequiredMixin',
    'UserRequestMixin',
    'UserLoginRequiredMixin',
    # Edit mixin
    'CsrfProtectMixin',
    'UserActionKwargsFormMixin',
    'HtmxDeleteView',
    'HtmxOwnerDeleteView',
    # View
    'BaseAddView',
    'BaseCreateView',
    'BaseUpdateView',
    'BaseListView',
]

from .auth import (
    OwnerMixin,
    OwnershipRequiredMixin,
    UserLoginRequiredMixin,
    UserRequestMixin,
)
from .crud import (
    BaseAddView,
    BaseCreateView,
    BaseListView,
    BaseUpdateView,
    CsrfProtectMixin,
    UserActionKwargsFormMixin,
)
from .htmx import (
    HtmxDeleteView,
    HtmxOwnerDeleteView,
)
