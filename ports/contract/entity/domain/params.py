"""Parameters interface."""

from typing import Protocol, TypeVar

Conditions_co = TypeVar('Conditions_co', covariant=True)
Config_co = TypeVar('Config_co', covariant=True)
Settings_co = TypeVar('Settings_co', covariant=True)


class HasConditions(Protocol[Conditions_co]):
    """Protocol for has *conditions* interface.

    Contains lookup conditions for domain.

    For example:
        - database lockup conditions
        - calculation operand conditions
    """

    @property
    def conditions(self) -> Conditions_co: ...  # noqa


class HasConfig(Protocol[Config_co]):
    """Protocol for has *config* interface.

    Contains configuration for domain.

    For example:
        - exercise's item count
        - item display order
    """

    @property
    def conf(self) -> Config_co: ...  # noqa


class HasSettings(Protocol[Settings_co]):
    """Protocol for has *settings* interface.

    Contains settings for user's interface to domain display.

    For example:
        - question / answer timeout
    """

    @property
    def settings(self) -> Settings_co: ...  # noqa


class GenericExerciseParameters(
    HasConditions[Conditions_co],
    HasConfig[Config_co],
    HasSettings[Settings_co],
    Protocol[Conditions_co, Config_co, Settings_co],
):
    """Generic exercise parameters.

    Parameters
    ----------
    conditions :
        Study resource lockup or task create conditions.
    conf :
        Exercise type domain configuration.
    settings :
        Exercise type perform settings.

    """
