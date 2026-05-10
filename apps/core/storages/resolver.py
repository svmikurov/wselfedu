"""Store key resolver."""

import hashlib
from typing import TypeVar

from ports.interfaces.schemas.command import UserCommand

from .abstract import AbstractStoreKeyResolver

Command = TypeVar('Command')
StoreKey = TypeVar('StoreKey')


HASH_SYMBOL_COUNT = 8


def generate_cache_key(prefix: str, user_id: int, **kwargs: object) -> str:
    """Generate a secure key with parameter hashing."""
    sorted_items = sorted(kwargs.items())
    param_string = ':'.join([f'{k}:{v}' for k, v in sorted_items])
    param_hash = hashlib.md5(param_string.encode()).hexdigest()[
        :HASH_SYMBOL_COUNT
    ]
    return f'{prefix}:{user_id}:{param_hash}'


class UserKeyCommandResolver(
    AbstractStoreKeyResolver[
        UserCommand,
        str,
    ],
):
    """Storage key resolver by command."""

    def resolve(
        self,
        command: UserCommand,
        prefix: str,
        **kwargs: object,
    ) -> str:
        """Resolve store key."""
        return generate_cache_key(prefix, command.user.pk, **kwargs)
