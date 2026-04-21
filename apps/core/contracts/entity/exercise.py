"""Exercise entity."""

from typing import Protocol, TypeVar

ExerciseConditionsT = TypeVar('ExerciseConditionsT')
ExerciseConfigT = TypeVar('ExerciseConfigT')
ExerciseSettingsT = TypeVar('ExerciseSettingsT')

# =================================================
# Exercise parameters DTO interface
# =================================================


class HasExerciseConditions(Protocol[ExerciseConditionsT]):
    """Protocol for has exercise conditions interface.

    Contains exercise elements select/define conditions.
    My contains:
        - database lockup conditions
        - calculation operand conditions
        - other conditions
    """

    conditions: ExerciseConditionsT


class HasExerciseConfig(Protocol[ExerciseConfigT]):
    """Protocol for has test exercise configuration interface.

    Contains display exercise configuration.
    For example:
        - question / answer timeout
        - other settings
    """

    conf: ExerciseConfigT


class HasExerciseSettings(Protocol[ExerciseSettingsT]):
    """Protocol for has exercise settings interface.

    Contains exercise display configuration, such as:
        - question / answer timeout
        - other settings
    """

    settings: ExerciseSettingsT
