"""Domain result formatter DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.core.formatters.exercise import PresentationFormatter, TestFormatter


class FormatterContainer(DeclarativeContainer):
    """Domain result formatter DI container."""

    # =============================================
    # Exercise domain result formatter
    # =============================================

    presentation = Factory(  # type: ignore
        PresentationFormatter,
    )
    test = Factory(  # type: ignore
        TestFormatter,
    )
