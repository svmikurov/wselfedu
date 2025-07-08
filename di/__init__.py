"""Contains the initialization of dependency injection."""

from di.di_container import CoreContainer

WIRED_MODULES = [
    'apps.math.api.v1.views',
]

container = CoreContainer()
