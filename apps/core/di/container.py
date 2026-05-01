"""Core application dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Factory

from utils.audit.impl import Auditor

from ..storages.clients.django_cache import DjangoCache, DjangoKeyCache
from ..storages.resolver import UserKeyCommandResolver
from ..storages.services.service import UserCommandStorage, UserDataStorage
from ..storages.services.task import TaskStorage
from .configuration import ConfigurationContainer
from .domain import DomainContainer


class CoreContainer(DeclarativeContainer):
    """Core application dependency injection container."""

    configuration = Container(
        ConfigurationContainer,
    )

    domains = Container(
        DomainContainer,
        exercise_config=configuration.exercise,
    )

    django_cache = Factory(  # type: ignore[var-annotated]
        DjangoCache,
    )
    django_key_cache = Factory(  # type: ignore[var-annotated]
        DjangoKeyCache,
    )

    # TODO: Rename to `django_cache`?
    task_storage = Factory(
        TaskStorage,
        storage=django_cache,
    )
    user_data_storage = Factory(
        UserDataStorage,
        storage=django_key_cache,
    )
    user_command_storage = Factory(
        UserCommandStorage,
        storage=django_key_cache,
        key_resolver=Factory(UserKeyCommandResolver),
    )

    auditor = Factory(Auditor)
