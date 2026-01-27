"""DI container for translation study via Presentation exercises.

Provides dependencies for handling WEB and API requests for exercises,
including:
    - Input validation for WEB and API requests
    - Exercise creation and progress tracking
    - Domain result adaptation for WEB and API responses
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from apps.lang.domain import presentation

from ... import adapters, repositories, services, use_cases, validators
from ...schemas import dto

type StoryCase = dto.CaseMeta

# HACK: Update on abstract a hint container dependency types
# REVIEW: Relocate the type hint definition to a separate module?
if TYPE_CHECKING:
    from apps.core.storage.clients import DjangoCache
    from apps.core.storage.services import TaskStorage

    from ...adapters import ApiPresentationAdapter, WebPresentationAdapter
    from ...domain import PresentationDomain
    from ...repositories import EnglishTranslation
    from ...services import PresentationService
    from ...use_cases import ApiPresentationUseCase, WebPresentationUseCase
    from ...validators import (
        ApiPresentationValidator,
        WebPresentationValidator,
    )

    # --------------------------------
    # Container dependencies type hint
    # --------------------------------

    # Validators
    type RegularValidatorFactory = Factory[WebPresentationValidator]
    type AssignedValidatorFactory = Factory[ApiPresentationValidator]

    # Service dependencies
    type DomainFactory = Factory[PresentationDomain]
    type TranslationRepositoryFactory = Factory[EnglishTranslation]
    type ProgressRepositoryFactory = Factory[DjangoCache[StoryCase]]
    type StorageFactory = Factory[TaskStorage[Any]]

    # Services
    type ServiceFactory = Factory[PresentationService]

    # Adapters
    type WebAdapterFactory = Factory[WebPresentationAdapter]
    type ApiAdapterFactory = Factory[ApiPresentationAdapter]

    # UseCases
    type WebUseCaseFactory = Factory[WebPresentationUseCase]
    type ApiUseCaseFactory = Factory[ApiPresentationUseCase]


class PresentationContainer(DeclarativeContainer):
    """Translation study presentation DI container."""

    # ---------------------
    # External dependencies
    # ---------------------

    # Current presentation case storage (Django cache)
    # Stores the ID of the translation for translation
    # study progress update.
    task_storage: Dependency[StorageFactory] = Dependency()

    # ------------------
    # Request Validators
    # ------------------

    # Validates presentation request, returns domain DTO.
    web_validator: RegularValidatorFactory = Factory(
        validators.WebPresentationValidator,
    )
    api_validator: AssignedValidatorFactory = Factory(
        validators.ApiPresentationValidator,
    )

    # --------------------
    # Service dependencies
    # --------------------

    # Repository to get presentation case candidates
    translation_repository = Factory(
        repositories.EnglishTranslation,
    )

    # Domain logic to get presentation case from candidates
    domain: DomainFactory = Factory(
        presentation.PresentationDomain,
    )

    # --------
    # Services
    # --------

    # Retrieves candidates for presentation case,
    # choices translation from candidates,
    # stores translation ID to updated progress,
    # returns translation case.
    exercise_service: ServiceFactory = Factory(
        services.PresentationService,
        repository=translation_repository,
        domain=domain,
        storage=task_storage,
    )

    # -----------------
    # Response Adapters
    # -----------------

    web_adapter: WebAdapterFactory = Factory(
        adapters.WebPresentationAdapter,
    )
    api_adapter: ApiAdapterFactory = Factory(
        adapters.ApiPresentationAdapter,
    )

    # ---------
    # Use cases
    # ---------

    web_use_case: WebUseCaseFactory = Factory(
        use_cases.WebPresentationUseCase,
        validator=web_validator,
        service=exercise_service,
        response_adapter=web_adapter,
    )
    api_use_case: ApiUseCaseFactory = Factory(
        use_cases.ApiPresentationUseCase,
        validator=api_validator,
        service=exercise_service,
        response_adapter=api_adapter,
    )
