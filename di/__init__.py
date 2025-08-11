"""Dependency injection configuration and container initialization.

Defines which modules should be wired and provides the DI container
instance.
"""

from di.di_container import MainContainer

WIRED_MODULES: list[str] = [
    'apps.math.api.v1.views.calculation',
    'apps.users.views.mentorship',
    'apps.users.views.assignation',
]

__all__ = [
    'MainContainer',
    'WIRED_MODULES',
]

container = MainContainer()
