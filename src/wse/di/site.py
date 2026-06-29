"""Django site entrypoint DI container.

Defines which modules should be wired and provides the DI container
instance.
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Factory

from wse.site import adapters, assemblers, handlers, validators

from . import application


class DjangoSiteContainer(DeclarativeContainer):
    """Django site entrypoint DI container."""

    # External dependencies

    use_cases = Container(
        application.ApplicationContainer,
    )

    # Internal dependencies

    null_validator = Factory(validators.NullValidator)
    null_assembler = Factory(assemblers.NullAssembler)
    null_adapter = Factory(adapters.NullAdapter)

    # Request handlers

    testing = Factory(
        handlers.ExerciseHandler,
        validator=null_validator,
        assembler=null_assembler,
        use_case=use_cases.create_testing,
        adapter=null_adapter,
    )
