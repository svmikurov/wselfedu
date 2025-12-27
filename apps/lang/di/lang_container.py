"""Language application DI container."""

from dependency_injector import containers, providers
from dependency_injector.providers import Container

from apps.core.storage import (
    clients as storage_clients,
)
from apps.core.storage import (
    services as storage,
)
from apps.lang import schemas

from .. import repositories, services
from .presentation import PresentationContainer

# TODO: Implement dynamic ttl in dependency
# as the sum of the question time and the answer time.
TRANSLATION_CASE_STORAGE_TTL = 600


class LanguageContainer(containers.DeclarativeContainer):
    """Language discipline DI container."""

    # ---------
    # Use cases
    # ---------

    presentation_container = Container(PresentationContainer)

    web_presentation_use_case = presentation_container.web_use_case
    api_presentation_use_case = presentation_container.api_use_case

    # --------------
    # Configurations
    # --------------

    progress_config = providers.Factory(
        schemas.ProgressConfigSchema,
        increment=1,
        decrement=1,
    )

    # --------------------
    # Storage dependencies
    # --------------------

    django_translation_cache = providers.Factory(
        storage_clients.DjangoCache[schemas.WordStudyStoredCase],
    )

    translation_study_storage = providers.Factory(
        storage.TaskStorage[schemas.WordStudyStoredCase],
        storage=django_translation_cache,
        ttl=TRANSLATION_CASE_STORAGE_TTL,
    )

    # ------------
    # Repositories
    # ------------

    parameters_repository = providers.Factory(
        repositories.StudyParametersRepository,
    )
    translation_repository = providers.Factory(
        repositories.TranslationRepository,
    )
    progress_repository = providers.Factory(
        repositories.Progress,
    )

    # --------
    # Services
    # --------

    progress_service = providers.Factory(
        services.UpdateWordProgressService,
        progress_repo=progress_repository,
        case_storage=translation_study_storage,
        progress_config=progress_config,
    )

    settings_service = providers.Factory(services.StudySettingsService)
