"""DI container for translation study via Test exercises.

Provides dependencies for handling WEB and API requests for exercises,
including:
    - Input validation for WEB and API requests
    - Exercise creation and progress tracking
    - Domain result adaptation for WEB and API responses
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory

from apps.core.storage import services as storage
from apps.core.storage.clients import DjangoCache
from apps.lang import adapters, repositories, services, use_cases, validators
from apps.lang.schemas.test import StoryDomainResult

# HACK: Replace Any type to hint container dependency types
# REVIEW: Relocate the type hint definition to a separate module?
if TYPE_CHECKING:
    from apps.lang.use_cases import types

    # --------------------------------
    # Container dependencies type hint
    # --------------------------------

    # Validators
    type RegularValidatorFactory = Factory[Any]
    type AssignedValidatorFactory = Factory[Any]

    # Service dependencies
    type TranslationRepositoryFactory = Factory[Any]
    type ProgressRepositoryFactory = Factory[Any]
    type StorageFactory = Factory[Any]

    # Services
    type RegularServiceFactory = Factory[Any]
    type AssignedServiceFactory = Factory[Any]
    type ProgressServiceFactory = Factory[Any]

    # Adapters
    type WebAdapterFactory = Factory[Any]

    # UseCases
    type WebRegularFactory = Factory[types.WebTest]
    type WebAssignedFactory = Factory[types.WebAssignedTest]
    type WebProgressFactory = Factory[Any]


# HACK: Split a container by a group of functional dependencies
class TranslationTestContainer(DeclarativeContainer):
    """Dependency injection container for translation test exercises."""

    # ---------------------------
    # Test exercise configuration
    # ---------------------------

    config = Configuration()

    # HACK: Replace the workaround of the exercise configuration
    config.from_dict(
        {
            'option_count': 5,
            'limit': 100,
            'case_storage_ttl': 600,
        }
    )

    # ------------------
    # Request Validators
    # ------------------

    web_regular_validator: RegularValidatorFactory = Factory(
        validators.WebTestValidator,
    )
    web_assigned_validator: AssignedValidatorFactory = Factory(
        validators.WebAssignedExerciseValidator,
    )

    # --------------------
    # Service dependencies
    # --------------------

    translation_repository: TranslationRepositoryFactory = Factory(
        repositories.TranslationRepository,
    )
    progress_repository: ProgressRepositoryFactory = Factory(
        repositories.Progress,
    )
    cache_client = Factory(
        DjangoCache[StoryDomainResult],
    )
    cache_storage: StorageFactory = Factory(
        storage.TaskStorage[StoryDomainResult],
        storage=cache_client,
        ttl=config.case_storage_ttl,
    )

    # --------
    # Services
    # --------

    regular_exercise_service: RegularServiceFactory = Factory(
        services.TestService,
        repository=translation_repository,
        storage=cache_storage,
        config=config,
    )
    assigned_exercise_service: AssignedServiceFactory = Factory(
        services.AssignedTestService,
        repository=translation_repository,
        storage=cache_storage,
        config=config,
    )

    progress_service: ProgressServiceFactory = Factory(
        services.TestProgressService,
        repository=translation_repository,
        progress_repository=progress_repository,
        storage=cache_storage,
        config=config,
    )

    # -----------------
    # Response Adapters
    # -----------------

    web_adapter: WebAdapterFactory = Factory(
        adapters.WebTestAdapter,
    )

    # --------
    # UseCases
    # --------

    web_regular_use_case: WebRegularFactory = Factory(
        use_cases.UseCase,
        validator=web_regular_validator,
        service=regular_exercise_service,
        response_adapter=web_adapter,
    )
    web_assigned_use_case: WebAssignedFactory = Factory(
        use_cases.DetailUseCase,
        validator=web_assigned_validator,
        service=assigned_exercise_service,
        response_adapter=web_adapter,
    )

    # Translation study have study progress tracking.
    web_progress_use_case: WebProgressFactory = Factory(
        use_cases.UseCase,
        validator=web_regular_validator,
        service=progress_service,
        response_adapter=web_adapter,
    )
