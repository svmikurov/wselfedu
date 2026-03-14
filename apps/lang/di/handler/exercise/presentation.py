"""DI container for translation study via Presentation exercises.

Provides dependencies for handling WEB and API requests for exercises,
including:
    - Input validation for WEB and API requests
    - Exercise creation and progress tracking
    - Domain result adaptation for WEB and API responses
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers import RequestHandler


class TranslationPresentationContainer(DeclarativeContainer):
    """Translation study presentation DI container."""

    validators = DependenciesContainer()
    use_cases = DependenciesContainer()
    adapters = DependenciesContainer()

    web_regular = Factory(
        RequestHandler,
        validator=validators.web_regular_presentation,
        use_case=use_cases.regular_translation_presentation,
        adapter=adapters.web_presentation,
    )
    api_regular = Factory(
        RequestHandler,
        validator=validators.api_regular_presentation,
        use_case=use_cases.regular_translation_presentation,
        adapter=adapters.api_presentation,
    )
