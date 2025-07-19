"""Contains the initialization of dependency injection."""

from di.di_container import CoreContainer

WIRED_MODULES: list[str] = []

container = CoreContainer()
