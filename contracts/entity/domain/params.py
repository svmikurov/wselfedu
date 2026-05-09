"""Parameters interface."""

from typing import Protocol, TypeVar

ConditionsT = TypeVar('ConditionsT', covariant=True)
ConfigT = TypeVar('ConfigT', covariant=True)
SettingsT = TypeVar('SettingsT', covariant=True)


class HasConditions(Protocol[ConditionsT]):
    """Protocol for has *conditions* interface.

    Contains lookup conditions for domain.

    For example:
        - database lockup conditions
        - calculation operand conditions
    """

    @property
    def conditions(self) -> ConditionsT: ...  # noqa


class HasConfig(Protocol[ConfigT]):
    """Protocol for has *config* interface.

    Contains configuration for domain.

    For example:
        - exercise's item count
        - item display order
    """

    @property
    def conf(self) -> ConfigT: ...  # noqa


class HasSettings(Protocol[SettingsT]):
    """Protocol for has *settings* interface.

    Contains settings for user's interface to domain display.

    For example:
        - question / answer timeout
    """

    @property
    def settings(self) -> SettingsT: ...  # noqa
