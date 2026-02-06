"""Adapter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory

from .. import adapters


class AdapterContainer(DeclarativeContainer):
    """Adapter DI container."""

    rule_config = Configuration()

    # ----------------
    # English language
    # ----------------

    web_rule = Factory(
        adapters.WebRuleAdapter,
        config=rule_config,
    )

    # -----------------
    # English exercises
    # -----------------

    web_test = Factory(
        adapters.WebTestAdapter,
    )
    web_presentation = Factory(
        adapters.WebPresentationAdapter,
    )
    api_presentation = Factory(
        adapters.ApiPresentationAdapter,
    )
