"""Language application DI container."""

from dependency_injector import containers
from dependency_injector.providers import Container

from ._adapter import AdapterContainer
from ._progress import ProgressContainer
from ._storage import StorageContainer
from .exercise.exercises import ExercisesContainer
from .repository import RepositoryContainer


class LanguageContainer(containers.DeclarativeContainer):
    """Language discipline DI container."""

    # The current exercise case is saved
    # to check the user's answer and change the study progress.
    storages = Container(StorageContainer)
    # QUESTION: Split the 'exercises' container
    # on 'presentation exercises', 'test exercises' or
    # on 'translation exercises', 'rule  exercises'?
    repositories = Container(
        RepositoryContainer,
    )
    adapters = Container(
        AdapterContainer,
    )

    exercises = Container(
        ExercisesContainer,
        exercise_case_storage=storages.exercise_case_storage,
        adapters=adapters,
    )
    progress = Container(
        ProgressContainer,
        exercise_case_storage=storages.exercise_case_storage,
    )
