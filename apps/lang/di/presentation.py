"""Get presentation UseCase DI container."""

from dependency_injector import containers, providers

from apps.core.storage import clients as storage_clients
from apps.core.storage import services as storage
from apps.lang.domain import presentation

from .. import adapters, repositories, services, use_cases, validators
from ..schemas import dto

type StoryCase = dto.CaseMeta

TRANSLATION_CASE_STORAGE_TTL = 600


class PresentationContainer(containers.DeclarativeContainer):
    """Get english presentation DI UseCase container."""

    # ----------------------------------------
    # Validators for presentation case request
    # ----------------------------------------

    # Validates presentation request, returns domain DTO.
    web_validator = providers.Factory(validators.WebPresentationValidator)
    api_validator = providers.Factory(validators.ApiPresentationValidator)

    # --------------------------------
    # Service to get presentation case
    # --------------------------------

    # Repository to get presentation case candidates
    eng_repository = providers.Factory(repositories.EnglishTranslation)

    # Domain logic to get presentation case from candidates
    domain = providers.Factory(presentation.PresentationDomain)

    # Current presentation case storage (Django cache)
    # Stores the ID of the translation for translation
    # study progress update.
    cache_client = providers.Factory(storage_clients.DjangoCache[StoryCase])
    cache_storage = providers.Factory(
        storage.TaskStorage[StoryCase],
        storage=cache_client,
        ttl=TRANSLATION_CASE_STORAGE_TTL,
    )

    # Service
    # Retrieves candidates for presentation case,
    # choices translation from candidates,
    # stores translation ID to updated progress,
    # returns translation case.
    eng_service = providers.Factory(
        services.PresentationService,
        repository=eng_repository,
        domain=domain,
        storage=cache_storage,
    )

    # -------------------------------------------
    # Presentation case data adapters to response
    # -------------------------------------------

    # Adapts presentation case for web & api response formats.
    web_adapter = providers.Factory(adapters.WebPresentationAdapter)
    api_adapter = providers.Factory(adapters.ApiPresentationAdapter)

    # ---------
    # Use cases
    # ---------

    # Provides api to get presentation case.
    web_use_case = providers.Factory(
        use_cases.WebPresentationUseCase,
        validator=web_validator,
        service=eng_service,
        response_adapter=web_adapter,
    )
    api_use_case = providers.Factory(
        use_cases.ApiPresentationUseCase,
        validator=api_validator,
        service=eng_service,
        response_adapter=api_adapter,
    )
