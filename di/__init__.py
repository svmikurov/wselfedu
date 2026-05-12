"""Dependency injection configuration and container initialization.

Defines which modules should be wired and provides the DI container
instance.
"""

from di.container import MainContainer

WIRED_MODULES: list[str] = [
    # =============================================
    # Glossary discipline
    # ---------------------------------------------
    'apps.glossary.api.v1.views.study',
    # =============================================
    # Language discipline
    # ---------------------------------------------
    'apps.lang.api.v1.views.study',
    'apps.lang.views.exercise.translation',
    'apps.lang.views.translation',
    # =============================================
    # Mathematical discipline
    # ---------------------------------------------
    'apps.math.api.v1.views.assigned',
    'apps.math.api.v1.views.calculation',
    'apps.math.views.exercise.calculation',
    # =============================================
    # Study application
    # ---------------------------------------------
    'apps.study.api.v1.views.assigned',
    # =============================================
    # Users application
    # ---------------------------------------------
    'apps.users.views.mentorship',
    'apps.users.views.assignation',
    # ---------------------------------------------
]

__all__ = (
    'MainContainer',
    'WIRED_MODULES',
)

container = MainContainer()
