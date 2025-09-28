"""Language application DI container."""

from dependency_injector import containers, providers

from .orchestrators import CreateEnglishTranslation


class LanguageContainer(containers.DeclarativeContainer):
    """Language discipline DI container."""

    translation_orchestrator = providers.Factory(
        CreateEnglishTranslation,
    )
