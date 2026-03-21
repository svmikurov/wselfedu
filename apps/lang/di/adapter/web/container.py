"""Language discipline web adapter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.lang.adapters import WebTestAdapter


class WebAdapterContainer(DeclarativeContainer):
    """Language discipline web adapter DI container."""

    # =============================================
    # English exercise
    # ---------------------------------------------
    test = Factory(
        WebTestAdapter,
    )
