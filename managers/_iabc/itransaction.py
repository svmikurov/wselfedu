"""Defines protocol and abc for transaction model manager."""

from typing import Protocol, TypeVar

from apps.users.models import Transaction

TransactionM_co = TypeVar(
    'TransactionM_co',
    bound=Transaction,
    covariant=True,
)
TransactionManagerT_co = TypeVar(
    'TransactionManagerT_co',
    bound='ITransactionManager[Transaction]',
    covariant=True,
)


class ITransactionManager(Protocol[TransactionM_co]):
    """Protocol for transaction model manager interface."""
