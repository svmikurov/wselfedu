"""DI container for translation study via Presentation exercises.

Provides dependencies for handling WEB and API requests for exercises,
including:
    - Input validation for WEB and API requests
    - Exercise creation and progress tracking
    - Domain result adaptation for WEB and API responses
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers import RegularRequestHandler


class TranslationPresentationContainer(DeclarativeContainer):
    """Translation study presentation DI container."""

    validators = DependenciesContainer()
    services = DependenciesContainer()
    adapters = DependenciesContainer()

    web_regular = Factory(
        RegularRequestHandler,
        validator=validators.web_regular_presentation,
        service=services.regular_translation_presentation,
        adapter=adapters.web_presentation,
    )
    api_regular = Factory(
        RegularRequestHandler,
        validator=validators.api_regular_presentation,
        service=services.regular_translation_presentation,
        adapter=adapters.api_presentation,
    )
