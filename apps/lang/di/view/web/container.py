"""View-injected exercise dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer


class WebViewContainer(DeclarativeContainer):
    """Language discipline web view dependencies."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    handlers = DependenciesContainer()

    # =============================================
    # English exercises
    # ---------------------------------------------
    start_regular_translation_test = handlers.start_regular_translation_test
