"""Adapter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from .. import adapters


class AdapterContainer(DeclarativeContainer):
    """Adapter DI container."""

    # ----------------
    # English language
    # ----------------

    web_rule = Factory(
        adapters.WebRuleAdapter,
        # HACK: Implement language rule configuration
        config={'example_count': None},
    )
    """Rule adapter for WEB response.
    """

    # ---------
    # Exercises
    # ---------

    web_test = Factory(adapters.WebTestAdapter)
    """Test exercise adapter for WEB response.
    """
