"""Validator DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.lang import validators


class ValidatorContainer(DeclarativeContainer):
    """Validator DI container."""

    # =============================================
    # Presentation exercises
    # ---------------------------------------------
    web_regular_presentation = Factory(validators.WebPresentationValidator)
    api_regular_presentation = Factory(validators.ApiPresentationValidator)

    # =============================================
    # Test exercises
    # ---------------------------------------------
    web_regular_test = Factory(validators.WebTestValidator)
    web_detail_test = Factory(validators.WebAssignedTestValidator)
