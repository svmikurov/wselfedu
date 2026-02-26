"""Configuration DI container."""

from typing import NamedTuple

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory

from ..domains.exercise import DisplayOrder, ProgressConfigSchema
from ..domains.exercise.types import Settings


# TODO: Remove this stub after implementation
# of global configuration of exercises.
# The named tuple allows for the use of dot annotation.
class ExerciseConfig(NamedTuple):
    """Exercise configuration."""

    display_order: DisplayOrder
    option_count: int
    item_count: int


# HACK: Implement a global configuration
class ConfigurationContainer(DeclarativeContainer):
    """Configuration DI container."""

    # Storage configuration
    # ---------------------

    storage = Configuration()
    storage.from_dict(
        {
            'case_storage_ttl': 600,
        }
    )

    # Rule display configuration
    # ---------------------------

    display_rule = Configuration()
    display_rule.from_dict(
        {
            'example_count': None,
        }
    )

    # Exercise configuration
    # ----------------------

    exercise: Settings = Factory(  # type: ignore
        ExerciseConfig,
        display_order=DisplayOrder.DEFINE,
        option_count=7,
        item_count=100,
    )

    # Update study progress configuration
    # -----------------------------------

    progress = Factory(
        ProgressConfigSchema,
        increment=1,
        decrement=1,
    )
