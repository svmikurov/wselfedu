"""DI container for translation study Validators."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.lang.validators import (
    WebAssignedTestValidator,
    WebTestValidator,
)


class TranslationValidatorContainer(DeclarativeContainer):
    """DI container for translation study Validators."""

    web_regular_validator = Factory(WebTestValidator)
    web_assigned_validator = Factory(WebAssignedTestValidator)
