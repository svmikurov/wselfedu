"""Defines the initialization of dependency injection containers."""

from di.di_container import MainContainer

# Initialization of the main container is lazy,
# which speeds up Django application startup,
# and initializes the container
# after the application is fully configured.
_container: MainContainer | None = None
_wired: bool = False


def init_container(modules_to_wire: list[str] | None = None) -> MainContainer:
    """Initialize the main container and wire.

    :param modules_to_wire: Modules for automatic dependency injection
      with `@inject` decorator
    :type modules_to_wire: list[str] | None
    :return: Initialized container
    :rtype: MainContainer
    """
    global _container, _wired

    if _container is not None:
        return _container

    # Container initialization
    _container = MainContainer()

    # Wiring modules
    if modules_to_wire is not None and not _wired:
        _container.wire(modules=modules_to_wire)
        _wired = True

    return _container


def get_container() -> MainContainer:
    """Return the initialized DI main container."""
    if _container is None:
        raise RuntimeError(
            'Container not initialized. Call init_container() first.'
        )
    return _container


def shutdown_container() -> None:
    """Clear the DI main container."""
    global _container, _wired
    if _container:
        _container.unwire()
    _container = None
    _wired = False
