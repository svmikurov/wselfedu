"""General typed data."""

from typing import Literal, TypedDict

type TranslationOrder = Literal['from_native', 'to_native', 'random']


# =================================================
# General data
# =================================================


class IdName(TypedDict):
    """Id-name option type."""

    id: int
    name: str


# =================================================
# Exercise data
# =================================================


class CodeName(TypedDict):
    """Code-name option type."""

    code: TranslationOrder
    name: str
