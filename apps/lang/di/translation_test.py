"""Translation study test exercise DI container."""

from dependency_injector import containers, providers

from apps.core.storage import services as storage
from apps.core.storage.clients import DjangoCache

from .. import adapters, repositories, services, use_cases, validators
from ..schemas.test import StoryDomainResult

CASE_STORAGE_TTL = 600


class TranslationTestContainer(containers.DeclarativeContainer):
    """Translation study test exercise DI container."""

    # ------------------
    # Test configuration
    # ------------------

    config = {
        'option_count': 7,
        'limit': 100,
    }

    # --------------------
    # Service dependencies
    # --------------------

    repository = providers.Factory(
        repositories.TranslationRepository,
    )

    cache_client = providers.Factory(DjangoCache[StoryDomainResult])
    cache_storage = providers.Factory(
        storage.TaskStorage[StoryDomainResult],
        storage=cache_client,
        ttl=CASE_STORAGE_TTL,
    )

    # --------------------
    # UseCase dependencies
    # --------------------

    web_validator = providers.Factory(validators.WebTestValidator)

    eng_service = providers.Factory(
        services.TestService,
        repository=repository,
        storage=cache_storage,
        config=config,
    )

    web_adapter = providers.Factory(adapters.WebTestAdapter)

    web_test = providers.Factory(
        use_cases.WebTestUseCase,
        validator=web_validator,
        service=eng_service,
        response_adapter=web_adapter,
    )
