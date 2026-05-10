"""Presentation types."""

from typing import Literal, TypedDict

type TranslationOrder = Literal['from_native', 'to_native', 'random']


# --------------
# Api data types
# --------------


class IdName(TypedDict):
    """Id-name option type."""

    id: int
    name: str


class CodeName(TypedDict):
    """Code-name option type."""

    code: TranslationOrder
    name: str
