"""Parameters interface."""

from typing import Protocol, TypeVar

ConditionsT = TypeVar('ConditionsT')
ConfigT = TypeVar('ConfigT')
SettingsT = TypeVar('SettingsT')


class HasConditions(Protocol[ConditionsT]):
    """Protocol for has *conditions* interface.

    Contains lookup conditions for domain.

    For example:
        - database lockup conditions
        - calculation operand conditions
    """

    conditions: ConditionsT


class HasConfig(Protocol[ConfigT]):
    """Protocol for has *config* interface.

    Contains configuration for domain.

    For example:
        - exercise's item count
        - item display order
    """

    conf: ConfigT


class HasSettings(Protocol[SettingsT]):
    """Protocol for has *settings* interface.

    Contains settings for user's interface to domain display.

    For example:
        - question / answer timeout
    """

    settings: SettingsT
