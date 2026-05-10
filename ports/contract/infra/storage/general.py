"""Protocol for storage service."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

T = TypeVar('T')
Command_contra = TypeVar('Command_contra', contravariant=True)
StoredObject_contra = TypeVar('StoredObject_contra', contravariant=True)
StoredObject_co = TypeVar('StoredObject_co', covariant=True)
StoredObject = TypeVar('StoredObject')


class SaveCommandStorageProtocol(
    Protocol[Command_contra, StoredObject_contra]
):
    """Protocol for save command storage interface."""

    def save(
        self,
        command: Command_contra,
        obj: StoredObject_contra,
        prefix: str,
        ttl: int | None = None,
        **kwargs: object,
    ) -> None:
        """Save data."""


class RetrieveCommandStorageProtocol(
    Protocol[Command_contra, StoredObject_co]
):
    """Protocol for retrieve command storage interface."""

    def retrieve(
        self,
        command: Command_contra,
        prefix: str,
        **kwargs: object,
    ) -> StoredObject_co:
        """Retrieve data."""


class OptionalRetrieveCommandStorageProtocol(
    Protocol[Command_contra, StoredObject_co]
):
    """Protocol for retrieve command storage interface."""

    def retrieve_or_none(
        self,
        command: Command_contra,
        prefix: str,
        **kwargs: object,
    ) -> StoredObject_co | None:
        """Retrieve data."""


class CommandStorageProtocol(
    Auditable,
    SaveCommandStorageProtocol[Command_contra, StoredObject],
    RetrieveCommandStorageProtocol[Command_contra, StoredObject],
    Protocol[Command_contra, StoredObject],
):
    """Protocol for command related storage interface."""
