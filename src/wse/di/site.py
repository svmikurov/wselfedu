"""Django site entrypoint DI container.

Defines which modules should be wired and provides the DI container
instance.
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Factory

from wse.site.handlers import ExerciseHandler

from . import application


class DjangoSiteContainer(DeclarativeContainer):
    """Django site entrypoint DI container."""

    use_cases = Container(
        application.ApplicationContainer,
    )

    testing = Factory(  # type: ignore[var-annotated]
        ExerciseHandler,
        use_case=use_cases.create_testing,
    )
