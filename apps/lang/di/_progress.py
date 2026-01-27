"""Study progress DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from ..repositories import Progress
from ..schemas import ProgressConfigSchema
from ..services import UpdateWordProgressService


class ProgressContainer(DeclarativeContainer):
    """Study progress DI container."""

    exercise_case_storage = Dependency()  # type: ignore[var-annotated]

    # ----------------------------------
    # Regular translation study progress
    # ----------------------------------

    regular_translation_config = Factory(
        ProgressConfigSchema,
        increment=1,
        decrement=1,
    )
    regular_translation_repository = Factory(Progress)
    regular_translation_service = Factory(
        UpdateWordProgressService,
        progress_repo=regular_translation_repository,
        # To change progress study, need
        # to get the current saved exercise
        case_storage=exercise_case_storage,
        progress_config=regular_translation_config,
    )
