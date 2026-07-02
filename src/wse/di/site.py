"""Django site entrypoint DI container.

Defines which modules should be wired and provides the DI container
instance.
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Factory

from wse.site.handlers import adapters, assemblers, generic, validators

from . import application


class DjangoSiteContainer(DeclarativeContainer):
    """Django site entrypoint DI container."""

    # External dependencies

    use_cases = Container(
        application.ApplicationContainer,
    )

    # Internal dependencies

    null_validator = Factory(
        validators.NullValidator,
    )
    create_testing_assembler = Factory(
        assemblers.CreateTestingTaskAssembler,
    )
    create_testing_adapter = Factory(
        adapters.CreateTestingAdapter,
        templates=['exercise/testing.html'],
    )

    # Request handlers

    testing = Factory(
        generic.RequestHandler,
        validator=null_validator,
        assembler=create_testing_assembler,
        use_case=use_cases.create_testing,
        adapter=create_testing_adapter,
    )
