"""Storage exceptions."""


class StorageError(Exception):
    """Base exception for storage operations."""

    pass


class CacheMissError(StorageError):
    """Raised when data is not found in cache."""

    pass


class StorageProgrammingError(StorageError):
    """Raised when programming error occurred."""

    pass
